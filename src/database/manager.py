"""
Database Manager
- SQLite operations with connection pooling
- Thread-safe database access
- Automatic retry logic
- Data persistence and querying
"""

import sqlite3
import threading
from datetime import datetime
from contextlib import contextmanager
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Thread-safe SQLite database manager"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._local = threading.local()
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with self.get_connection() as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS discovered_pools (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        address TEXT UNIQUE NOT NULL,
                        token0 TEXT NOT NULL,
                        token1 TEXT NOT NULL,
                        fee INTEGER NOT NULL,
                        initial_liquidity INTEGER DEFAULT 0,
                        current_liquidity INTEGER DEFAULT 0,
                        is_tradeable BOOLEAN DEFAULT FALSE,
                        discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS notification_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pool_address TEXT NOT NULL,
                        notification_type TEXT NOT NULL,
                        success BOOLEAN NOT NULL,
                        channels TEXT,
                        error TEXT,
                        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_pools_address 
                    ON discovered_pools(address)
                ''')
                
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_pools_tradeable 
                    ON discovered_pools(is_tradeable)
                ''')
                
                conn.commit()
                logger.info("✅ Database initialized successfully")
                
        except sqlite3.Error as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
                timeout=30.0
            )
            self._local.connection.row_factory = sqlite3.Row
        
        try:
            yield self._local.connection
        except Exception as e:
            self._local.connection.rollback()
            raise
        finally:
            # Don't close connection here, keep it for reuse
            pass
    
    def save_pool(self, pool_data: Dict) -> bool:
        """Save discovered pool to database"""
        try:
            with self.get_connection() as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO discovered_pools 
                    (address, token0, token1, fee, initial_liquidity, current_liquidity, is_tradeable)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    pool_data['address'],
                    pool_data['token0'],
                    pool_data['token1'],
                    pool_data['fee'],
                    pool_data['liquidity'],
                    pool_data['liquidity'],
                    pool_data['liquidity'] >= 1000  # Default threshold
                ))
                conn.commit()
                logger.debug(f"💾 Pool saved: {pool_data['address']}")
                return True
                
        except sqlite3.Error as e:
            logger.error(f"❌ Failed to save pool {pool_data.get('address', 'unknown')}: {e}")
            return False
    
    def get_non_tradeable_pools(self) -> List[Dict]:
        """Get pools that are not yet tradeable"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute('''
                    SELECT * FROM discovered_pools 
                    WHERE is_tradeable = FALSE
                    ORDER BY discovered_at DESC
                ''')
                return [dict(row) for row in cursor.fetchall()]
                
        except sqlite3.Error as e:
            logger.error(f"❌ Failed to fetch non-tradeable pools: {e}")
            return []
    
    def mark_pool_tradeable(self, pool_address: str, liquidity: int) -> bool:
        """Mark pool as tradeable with updated liquidity"""
        try:
            with self.get_connection() as conn:
                conn.execute('''
                    UPDATE discovered_pools 
                    SET is_tradeable = TRUE, 
                        current_liquidity = ?,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE address = ?
                ''', (liquidity, pool_address))
                conn.commit()
                logger.info(f"✅ Pool marked tradeable: {pool_address}")
                return True
                
        except sqlite3.Error as e:
            logger.error(f"❌ Failed to mark pool tradeable {pool_address}: {e}")
            return False
    
    def log_notification(self, pool_address: str, notification_type: str, 
                        success: bool, channels: str, error: str = None) -> bool:
        """Log notification attempt"""
        try:
            with self.get_connection() as conn:
                conn.execute('''
                    INSERT INTO notification_log 
                    (pool_address, notification_type, success, channels, error)
                    VALUES (?, ?, ?, ?, ?)
                ''', (pool_address, notification_type, success, channels, error))
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            logger.error(f"❌ Failed to log notification: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        try:
            with self.get_connection() as conn:
                stats = {}
                
                # Pool stats
                cursor = conn.execute('SELECT COUNT(*) FROM discovered_pools')
                stats['total_pools'] = cursor.fetchone()[0]
                
                cursor = conn.execute('SELECT COUNT(*) FROM discovered_pools WHERE is_tradeable = TRUE')
                stats['tradeable_pools'] = cursor.fetchone()[0]
                
                # Notification stats
                cursor = conn.execute('SELECT COUNT(*) FROM notification_log WHERE success = TRUE')
                stats['successful_notifications'] = cursor.fetchone()[0]
                
                cursor = conn.execute('SELECT COUNT(*) FROM notification_log WHERE success = FALSE')
                stats['failed_notifications'] = cursor.fetchone()[0]
                
                return stats
                
        except sqlite3.Error as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}
    
    def close(self):
        """Close database connections"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close() 
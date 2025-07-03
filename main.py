"""
Enhanced Pool Listener - Main Entry Point
Professional modular architecture with clean separation of concerns
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import load_settings
from database import DatabaseManager
from notifications import NotificationManager
from blockchain import PoolMonitor, Web3Client
from metrics import MetricsServer
from utils import setup_logging

async def main():
    """Main application entry point"""
    
    try:
        # Load configuration
        settings = load_settings()
        
        # Setup logging
        logger = setup_logging(settings.log_level)
        logger.info("🚀 Starting Enhanced Pool Listener")
        
        # Initialize components
        db = DatabaseManager(settings.database_path)
        web3_client = Web3Client(settings.infura_url)
        notification_manager = NotificationManager(settings)
        metrics_server = MetricsServer(settings.metrics_port)
        
        # Set token symbol for dashboard display
        metrics_server.set_token_symbol(settings.token_symbol)
        
        # Start metrics server
        metrics_server.start()
        
        # Initialize pool monitor with all dependencies
        pool_monitor = PoolMonitor(
            web3_client=web3_client,
            db=db,
            notification_manager=notification_manager,
            settings=settings,
            metrics_server=metrics_server  # Pass metrics server to pool monitor
        )
        
        logger.info("✅ All components initialized successfully")
        
        # Start monitoring
        await pool_monitor.start_monitoring()
        
    except KeyboardInterrupt:
        logger.info("👋 Shutting down gracefully...")
        if 'metrics_server' in locals():
            metrics_server.stop()
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        if 'metrics_server' in locals():
            metrics_server.stop()
        raise

if __name__ == "__main__":
    asyncio.run(main()) 
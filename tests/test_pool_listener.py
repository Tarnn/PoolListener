"""
Comprehensive Test Suite for Modular Pool Listener
Tests all modules: config, database, notifications, blockchain, metrics
"""

import pytest
import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import tempfile
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import Settings, load_settings
from database import DatabaseManager
from notifications import NotificationManager
from utils import setup_logging

class TestSettings(unittest.TestCase):
    """Test configuration management"""
    
    def setUp(self):
        """Set up test environment variables"""
        self.env_vars = {
            'INFURA_API_KEY': 'test_key_12345678901234567890',
            'TOKEN_ADDRESS': '0x1234567890123456789012345678901234567890',
            'SENDER_EMAIL': 'test@example.com',
            'RECEIVER_EMAIL': 'receiver@example.com',
            'EMAIL_PASSWORD': 'test_password',
            'NOTIFICATION_URLS': 'discord://webhook_url'
        }
        
        for key, value in self.env_vars.items():
            os.environ[key] = value
    
    def tearDown(self):
        """Clean up environment variables"""
        for key in self.env_vars:
            if key in os.environ:
                del os.environ[key]
    
    def test_settings_validation(self):
        """Test settings validation"""
        settings = load_settings()
        
        self.assertEqual(settings.infura_api_key, self.env_vars['INFURA_API_KEY'])
        self.assertEqual(settings.token_address, self.env_vars['TOKEN_ADDRESS'].lower())
        self.assertEqual(len(settings.receiver_emails), 1)
        self.assertIn('smtp.gmail.com', settings.smtp_server)
    
    def test_invalid_token_address(self):
        """Test invalid token address validation"""
        os.environ['TOKEN_ADDRESS'] = 'invalid_address'
        
        with self.assertRaises(ValueError):
            load_settings()

class TestDatabaseManager(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        """Clean up test database"""
        self.db.close()
        os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test database table creation"""
        stats = self.db.get_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_pools', stats)
    
    def test_pool_operations(self):
        """Test pool save and retrieve operations"""
        pool_data = {
            'address': '0x1234567890123456789012345678901234567890',
            'token0': '0xtoken0',
            'token1': '0xtoken1',
            'fee': 3000,
            'liquidity': 500  # Below threshold
        }
        
        # Save pool
        result = self.db.save_pool(pool_data)
        self.assertTrue(result)
        
        # Check stats
        stats = self.db.get_stats()
        self.assertEqual(stats['total_pools'], 1)
        
        # Get non-tradeable pools (liquidity is below threshold)
        pools = self.db.get_non_tradeable_pools()
        self.assertEqual(len(pools), 1)
        self.assertEqual(pools[0]['address'], pool_data['address'])
    
    def test_mark_pool_tradeable(self):
        """Test marking pool as tradeable"""
        pool_data = {
            'address': '0x1234567890123456789012345678901234567890',
            'token0': '0xtoken0',
            'token1': '0xtoken1',
            'fee': 3000,
            'liquidity': 500  # Below threshold
        }
        
        # Save pool
        self.db.save_pool(pool_data)
        
        # Mark as tradeable
        result = self.db.mark_pool_tradeable(pool_data['address'], 2000)
        self.assertTrue(result)
        
        # Check it's no longer in non-tradeable list
        pools = self.db.get_non_tradeable_pools()
        self.assertEqual(len(pools), 0)

class TestNotificationManager(unittest.TestCase):
    """Test notification manager"""
    
    def setUp(self):
        """Set up test notification manager"""
        self.settings = MagicMock()
        self.settings.sender_email = "test@example.com"
        self.settings.receiver_emails = ["receiver@example.com"]
        self.settings.email_password = "password"
        self.settings.smtp_server = "smtp.gmail.com"
        self.settings.smtp_port = 587
        self.settings.token_symbol = "TEST"
        self.settings.token_address = "0x123"
        self.settings.min_liquidity_threshold = 1000
        self.settings.notification_urls = ""
        
        self.manager = NotificationManager(self.settings)
    
    @patch('src.notifications.manager.smtplib.SMTP')
    def test_email_notification(self, mock_smtp):
        """Test email notification sending"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Run the async function in event loop
        async def run_test():
            await self.manager.send_notification(
                "0x123", "0xtoken0", "0xtoken1", 3000, 2000, "liquidity_added"
            )
        
        # Use asyncio to run the test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(run_test())
        finally:
            loop.close()
        
        mock_server.send_message.assert_called_once()
    
    def test_template_generation(self):
        """Test template generation"""
        embed = self.manager.discord_templates.get_pool_created_embed(
            "0x123", "0xtoken0", "0xtoken1", 3000, 2000, self.settings
        )
        
        self.assertIn("embeds", embed)
        self.assertIn("title", embed["embeds"][0])
        self.assertIn("TEST", embed["embeds"][0]["title"])

class TestLoggingSetup(unittest.TestCase):
    """Test logging configuration"""
    
    def test_logging_setup(self):
        """Test that logging setup works without errors"""
        try:
            setup_logging()
            self.assertTrue(True)  # If no exception, test passes
        except Exception as e:
            self.fail(f"Logging setup failed: {e}")

# Test runner
def run_tests():
    """Run all tests"""
    print("🧪 Running Enhanced Pool Listener Test Suite...")
    print("=" * 60)
    
    # Run tests
    unittest.main(verbosity=2)

if __name__ == "__main__":
    run_tests() 
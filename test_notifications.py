#!/usr/bin/env python3
"""
Real Notification Test Script
Tests actual email and Discord notifications with your configured settings
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import load_settings
from notifications import NotificationManager
from utils import setup_logging

async def test_notifications():
    """Test actual notifications with real credentials"""
    print("🧪 Testing Real Notifications")
    print("=" * 50)
    
    # Setup logging
    setup_logging()
    
    # Load settings
    try:
        settings = load_settings()
        print(f"✅ Settings loaded successfully")
        print(f"📧 Email: {settings.sender_email}")
        print(f"📱 Discord: {'Configured' if settings.notification_urls else 'Not configured'}")
    except Exception as e:
        print(f"❌ Failed to load settings: {e}")
        return False
    
    # Create notification manager
    try:
        notification_manager = NotificationManager(settings)
        print(f"✅ Notification manager created")
    except Exception as e:
        print(f"❌ Failed to create notification manager: {e}")
        return False
    
    # Test data
    test_pool_address = "0x1234567890123456789012345678901234567890"
    test_token0 = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # WETH
    test_token1 = settings.token_address  # Your token
    test_fee = 3000  # 0.3%
    test_liquidity = 15000  # Above threshold
    
    print("\n🚀 Sending test notifications...")
    print(f"📍 Test Pool: {test_pool_address}")
    print(f"💰 Test Liquidity: {test_liquidity:,}")
    print(f"🎯 Target: {settings.token_symbol}")
    
    # Test 1: Pool Created Notification
    print("\n📧 Test 1: Pool Created Notification")
    try:
        await notification_manager.send_notification(
            pool_address=test_pool_address,
            token0=test_token0,
            token1=test_token1,
            fee=test_fee,
            liquidity=test_liquidity,
            notification_type="pool_created"
        )
        print("✅ Pool Created notification sent successfully!")
    except Exception as e:
        print(f"❌ Pool Created notification failed: {e}")
        return False
    
    # Wait a bit between notifications
    await asyncio.sleep(3)
    
    # Test 2: Liquidity Added Notification
    print("\n🔥 Test 2: Liquidity Added (TRADEABLE) Notification")
    try:
        await notification_manager.send_notification(
            pool_address=test_pool_address,
            token0=test_token0,
            token1=test_token1,
            fee=test_fee,
            liquidity=test_liquidity,
            notification_type="liquidity_added"
        )
        print("✅ Liquidity Added notification sent successfully!")
    except Exception as e:
        print(f"❌ Liquidity Added notification failed: {e}")
        return False
    
    print("\n🎉 All notifications sent successfully!")
    print("📧 Check your email inbox")
    print("📱 Check your Discord channel")
    
    return True

if __name__ == "__main__":
    print("🧪 Real Notification Test")
    print("This will send actual emails and Discord messages!")
    print("=" * 60)
    
    # Run the test
    success = asyncio.run(test_notifications())
    
    if success:
        print("\n✅ NOTIFICATION TEST PASSED!")
        print("🎯 Your Pool Listener notifications are working perfectly!")
    else:
        print("\n❌ NOTIFICATION TEST FAILED!")
        print("🔧 Please check your .env configuration")
    
    sys.exit(0 if success else 1) 
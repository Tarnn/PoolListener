#!/usr/bin/env python3
"""
Debug Email Recipients
Check how email parsing is working
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import load_settings

def debug_email_settings():
    """Debug email recipient parsing"""
    print("🔍 Debugging Email Recipients")
    print("=" * 40)
    
    try:
        settings = load_settings()
        
        print(f"📧 Sender Email: {settings.sender_email}")
        print(f"📝 Raw RECEIVER_EMAIL: {getattr(settings, '_raw_receiver_email', 'Not available')}")
        print(f"📋 Parsed Recipients: {settings.receiver_emails}")
        print(f"🔢 Number of Recipients: {len(settings.receiver_emails)}")
        
        print("\n📍 Individual Recipients:")
        for i, email in enumerate(settings.receiver_emails, 1):
            print(f"  {i}. '{email}' (length: {len(email)})")
            
        # Test email sending setup
        print(f"\n🔧 SMTP Settings:")
        print(f"  Server: {settings.smtp_server}")
        print(f"  Port: {settings.smtp_port}")
        print(f"  Password Length: {len(settings.email_password)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        return False

if __name__ == "__main__":
    debug_email_settings() 
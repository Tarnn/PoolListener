#!/usr/bin/env python3
"""
Test Individual Email Sending
Send to each recipient separately to debug the issue
"""

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from config import load_settings

async def test_individual_emails():
    """Test sending to each email individually"""
    print("🧪 Testing Individual Email Sending")
    print("=" * 50)
    
    try:
        settings = load_settings()
        print(f"📧 Sender: {settings.sender_email}")
        print(f"🔢 Recipients: {len(settings.receiver_emails)}")
        
        for i, recipient in enumerate(settings.receiver_emails, 1):
            print(f"\n📧 Test {i}: Sending to '{recipient}'")
            
            try:
                # Create test message
                msg = MIMEMultipart()
                msg['Subject'] = f"🔍 Pool Listener Test {i} - Individual Email"
                msg['From'] = settings.sender_email
                msg['To'] = recipient
                
                # HTML body
                html_body = f"""
                <html>
                <body>
                    <h2>🔍 Pool Listener Individual Email Test {i}</h2>
                    <p><strong>To:</strong> {recipient}</p>
                    <p><strong>From:</strong> {settings.sender_email}</p>
                    <p><strong>Time:</strong> {asyncio.get_event_loop().time()}</p>
                    
                    <p>This is test {i} of {len(settings.receiver_emails)} individual emails.</p>
                    
                    {"<p><strong>⚠️ NOTE:</strong> This email is being sent to the same account as the sender. Gmail might filter this into Spam or combine it with other emails.</p>" if recipient == settings.sender_email else ""}
                    
                    <p>✅ If you're seeing this, individual email {i} is working!</p>
                </body>
                </html>
                """
                
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
                
                # Send email
                with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
                    server.starttls()
                    server.login(settings.sender_email, settings.email_password)
                    server.send_message(msg)
                
                print(f"   ✅ Successfully sent to {recipient}")
                
                # Small delay between emails
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Failed to send to {recipient}: {e}")
        
        print(f"\n🎉 Individual email test completed!")
        print(f"📧 Check both inboxes:")
        print(f"   1. {settings.receiver_emails[0]} (might be in Sent folder)")
        print(f"   2. {settings.receiver_emails[1]} (should be in Inbox)")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_individual_emails()) 
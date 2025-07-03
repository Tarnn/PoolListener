import apprise
import os
from dotenv import load_dotenv

load_dotenv()

def test_dual_notifications():
    """Test both email and Discord notifications together"""
    
    apobj = apprise.Apprise()
    
    # Add email notifications
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_emails = os.getenv('RECEIVER_EMAIL').split(',')
    
    for recipient in receiver_emails:
        apobj.add(f"mailto://{recipient.strip()}")
        print(f"📧 Added email: {recipient.strip()}")
    
    # Add Discord webhook
    discord_url = "discord://1390128714032877599/4aj3GoqaaDrFD5e2jEW5rc7V0A6LYasLvRb54dzvRRGClUScZ1-tgrsabN5uaXJQ4NSY"
    apobj.add(discord_url)
    print("📱 Added Discord webhook")
    
    print(f"\n🔢 Total channels configured: {len(apobj.servers)}")
    
    # Send test notification to ALL channels
    title = "🧪 Dual Notification Test"
    body = """✅ BOTH Email + Discord Working!

📧 This message was sent to your email(s)
📱 This message was sent to your Discord channel

🚀 Your Enhanced Pool Listener will now notify you via:
• Email inbox
• Discord #pool-listener channel

Ready for pool monitoring! 🎉"""
    
    success = apobj.notify(title=title, body=body)
    
    if success:
        print("\n✅ SUCCESS: Both email and Discord notifications sent!")
        print("Check both your email inbox AND Discord channel")
    else:
        print("\n❌ FAILED: Something went wrong with notifications")
    
    return success, len(apobj.servers)

if __name__ == "__main__":
    success, channel_count = test_dual_notifications()
    print(f"\nResult: {channel_count} channels, Success: {success}") 
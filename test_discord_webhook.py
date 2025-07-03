import apprise
import os
from dotenv import load_dotenv

load_dotenv()

# Test Discord webhook
def test_discord_notification():
    apobj = apprise.Apprise()
    
    # Add your Discord webhook
    discord_url = "discord://1390128714032877599/4aj3GoqaaDrFD5e2jEW5rc7V0A6LYasLvRb54dzvRRGClUScZ1-tgrsabN5uaXJQ4NSY"
    apobj.add(discord_url)
    
    # Test message
    title = "🧪 Pool Listener Test"
    body = """🎉 Discord Integration Test Successful!

📊 Your Enhanced Pool Listener is now configured to send notifications to:
• Discord channel: pool-listener
• Webhook ID: 1390128714032877599

🚀 Ready to monitor for new pools!"""
    
    # Send test notification
    success = apobj.notify(title=title, body=body)
    
    if success:
        print("✅ Discord webhook test successful!")
        print("Check your Discord channel for the test message.")
    else:
        print("❌ Discord webhook test failed!")
        print("Please check your webhook URL and permissions.")
    
    return success

if __name__ == "__main__":
    test_discord_notification() 
"""
Notification Manager
- Multi-channel notification sending
- Beautiful template rendering
- Retry logic and error handling
"""

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import apprise
import backoff

from .templates.discord import DiscordTemplates
from .templates.email import EmailTemplates

logger = logging.getLogger(__name__)

class NotificationManager:
    """Manage multi-channel notifications with beautiful templates"""
    
    def __init__(self, settings):
        self.settings = settings
        self.apobj = apprise.Apprise()
        self.discord_templates = DiscordTemplates()
        self.email_templates = EmailTemplates()
        self.setup_channels()
    
    def setup_channels(self):
        """Setup notification channels"""
        
        # Email is always enabled
        logger.info(f"📧 Email notifications enabled for {len(self.settings.receiver_emails)} recipients")
        
        # Additional channels from environment
        if self.settings.notification_urls:
            for url in self.settings.notification_urls.split(','):
                if url.strip():
                    try:
                        self.apobj.add(url.strip())
                        logger.info(f"📱 Added notification channel: {url.strip()[:30]}...")
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to add channel {url.strip()[:30]}...: {e}")
        
        logger.info(f"✅ Total notification channels: {len(self.apobj.servers) + 1}")  # +1 for email
    
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    async def send_notification(self, pool_address: str, token0: str, token1: str, 
                              fee: int, liquidity: int, notification_type: str):
        """Send beautiful multi-channel notifications"""
        
        try:
            # Send email notification first (most reliable)
            await self._send_email_notification(
                pool_address, token0, token1, fee, liquidity, notification_type
            )
            
            # Send to all other channels (Discord, etc.)
            await self._send_other_notifications(
                pool_address, token0, token1, fee, liquidity, notification_type
            )
            
            logger.info(f"✅ All notifications sent successfully for {pool_address}")
            
        except Exception as e:
            logger.error(f"❌ Notification sending failed: {e}")
            raise
    
    async def _send_email_notification(self, pool_address: str, token0: str, token1: str,
                                     fee: int, liquidity: int, notification_type: str):
        """Send beautiful HTML email"""
        try:
            # Get email template
            if notification_type == "pool_created":
                subject, html_body = self.email_templates.get_pool_created_email(
                    pool_address, token0, token1, fee, liquidity, self.settings
                )
            else:
                subject, html_body = self.email_templates.get_liquidity_added_email(
                    pool_address, token0, token1, fee, liquidity, self.settings
                )
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.settings.sender_email
            msg['To'] = ', '.join(self.settings.receiver_emails)
            
            # Attach HTML
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port) as server:
                server.starttls()
                server.login(self.settings.sender_email, self.settings.email_password)
                server.send_message(msg)
            
            logger.info(f"📧 Beautiful HTML email sent to {len(self.settings.receiver_emails)} recipients")
            
        except Exception as e:
            logger.error(f"❌ Email sending failed: {e}")
            raise
    
    async def _send_other_notifications(self, pool_address: str, token0: str, token1: str,
                                      fee: int, liquidity: int, notification_type: str):
        """Send to all other notification channels (Discord, Slack, etc.)"""
        try:
            if not self.apobj.servers:
                logger.debug("No additional notification channels configured")
                return
            
            # Get message for channels
            subject, message = self._get_channel_message(
                pool_address, token0, token1, fee, liquidity, notification_type
            )
            
            # Send via Apprise to all channels
            success = self.apobj.notify(title=subject, body=message)
            
            if success:
                logger.info(f"📱 Notifications sent to {len(self.apobj.servers)} channels (Discord, etc.)")
            else:
                logger.warning(f"⚠️ Some notifications to external channels failed")
                    
        except Exception as e:
            logger.error(f"❌ External notifications failed: {e}")
    
    def _get_channel_message(self, pool_address: str, token0: str, token1: str,
                           fee: int, liquidity: int, notification_type: str) -> tuple[str, str]:
        """Get subject and message for notification channels"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        if notification_type == "pool_created":
            subject = f"🔍 {self.settings.token_symbol} Pool Discovered"
            message = f"""**{self.settings.token_symbol} Pool Discovered!**

🕒 **Time:** {timestamp}
📍 **Pool:** `{pool_address}`
💸 **Fee:** {fee/10000:.2f}% ({fee} basis points)
💰 **Liquidity:** {liquidity:,} {'🔥 **TRADEABLE!**' if liquidity >= self.settings.min_liquidity_threshold else '⚠️ *Monitoring...*'}

🔄 **Trade Now:** https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={self.settings.token_address}"""
            
        else:  # liquidity_added
            subject = f"🚀 {self.settings.token_symbol} NOW TRADEABLE! 🔥"
            message = f"""**🏆 TRADING ALERT: {self.settings.token_symbol} IS NOW TRADEABLE! 🚀**

**Pool has sufficient liquidity for trading!**

🕒 **Time:** {timestamp}
📍 **Pool:** `{pool_address}`
💰 **Liquidity:** {liquidity:,} - **READY TO TRADE!**

⚡ **TRADE NOW:** https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={self.settings.token_address}

🎯 This is your moment - the pool is ready for trading!"""
        
        return subject, message 
"""
Professional-Grade Notification Templates
- Rich Discord Embeds with proper colors and formatting
- Beautiful HTML Email Templates with visual hierarchy
- Consistent branding and emoji strategy
"""

from datetime import datetime
import json
from typing import Dict, Any

class NotificationTemplates:
    """Professional notification templates for Pool Listener"""
    
    # Brand Colors (Professional Trading Theme)
    COLORS = {
        'success': 0x00FF88,      # Bright Green - Trading Success
        'monitoring': 0x3498DB,   # Professional Blue - Monitoring
        'warning': 0xF39C12,      # Amber - Warning
        'error': 0xE74C3C,        # Red - Error
        'info': 0x9B59B6         # Purple - Information
    }
    
    # Emoji Strategy
    EMOJIS = {
        'pool_created': '🔍',
        'liquidity_added': '🚀',
        'money': '💰',
        'chart': '📊',
        'fire': '🔥',
        'diamond': '💎',
        'rocket': '🚀',
        'eyes': '👀',
        'lightning': '⚡',
        'trophy': '🏆'
    }
    
    @staticmethod
    def get_discord_embed(pool_address: str, token0: str, token1: str, fee: int, 
                         liquidity: int, notification_type: str, settings) -> Dict[str, Any]:
        """Create rich Discord embed"""
        
        timestamp = datetime.now().isoformat()
        
        if notification_type == "pool_created":
            return NotificationTemplates._get_pool_created_embed(
                pool_address, token0, token1, fee, liquidity, settings, timestamp
            )
        else:  # liquidity_added
            return NotificationTemplates._get_liquidity_added_embed(
                pool_address, token0, token1, fee, liquidity, settings, timestamp
            )
    
    @staticmethod
    def _get_pool_created_embed(pool_address: str, token0: str, token1: str, 
                               fee: int, liquidity: int, settings, timestamp: str) -> Dict[str, Any]:
        """Rich embed for pool creation"""
        
        is_tradeable = liquidity >= settings.min_liquidity_threshold
        
        return {
            "embeds": [{
                "title": f"🔍 {settings.token_symbol} Pool Discovered",
                "description": f"**New pool found - Now monitoring for liquidity**",
                "color": NotificationTemplates.COLORS['monitoring'],
                "timestamp": timestamp,
                "thumbnail": {
                    "url": "https://raw.githubusercontent.com/Uniswap/assets/master/blockchains/ethereum/assets/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984/logo.png"
                },
                "fields": [
                    {
                        "name": "🎯 Pool Address",
                        "value": f"```{pool_address}```",
                        "inline": False
                    },
                    {
                        "name": "🪙 Token Pair",
                        "value": f"**Token A:** `{token0[:6]}...{token0[-4:]}`\n**Token B:** `{token1[:6]}...{token1[-4:]}`",
                        "inline": True
                    },
                    {
                        "name": "💸 Fee Tier",
                        "value": f"**{fee/10000:.2f}%** ({fee} basis points)",
                        "inline": True
                    },
                    {
                        "name": "💰 Current Liquidity",
                        "value": f"**{liquidity:,}**" + (
                            f" {NotificationTemplates.EMOJIS['fire']} **TRADEABLE!**" if is_tradeable 
                            else f" ⚠️ *Below threshold ({settings.min_liquidity_threshold:,})*"
                        ),
                        "inline": False
                    },
                    {
                        "name": "🔗 Quick Actions",
                        "value": (
                            f"[📊 View on Etherscan](https://etherscan.io/address/{pool_address}) • "
                            f"[🏊 Uniswap Pool](https://app.uniswap.org/#/pool/{pool_address}) • "
                            f"[🔄 Trade Now](https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={settings.token_address})"
                        ),
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"Enhanced Pool Listener • {settings.token_symbol} Monitor",
                    "icon_url": "https://raw.githubusercontent.com/ethereum/ethereum-org-website/dev/src/assets/assets/eth-diamond-purple.png"
                }
            }]
        }
    
    @staticmethod
    def _get_liquidity_added_embed(pool_address: str, token0: str, token1: str, 
                                  fee: int, liquidity: int, settings, timestamp: str) -> Dict[str, Any]:
        """Rich embed for liquidity added (tradeable)"""
        
        return {
            "embeds": [{
                "title": f"🚀 {settings.token_symbol} NOW TRADEABLE!",
                "description": f"**{NotificationTemplates.EMOJIS['fire']} Pool has sufficient liquidity - Ready to trade! {NotificationTemplates.EMOJIS['diamond']}**",
                "color": NotificationTemplates.COLORS['success'],
                "timestamp": timestamp,
                "thumbnail": {
                    "url": "https://raw.githubusercontent.com/Uniswap/assets/master/blockchains/ethereum/assets/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984/logo.png"
                },
                "fields": [
                    {
                        "name": f"{NotificationTemplates.EMOJIS['trophy']} TRADING ALERT",
                        "value": f"**{settings.token_symbol} is now tradeable with {liquidity:,} liquidity!**",
                        "inline": False
                    },
                    {
                        "name": "🎯 Pool Address",
                        "value": f"```{pool_address}```",
                        "inline": False
                    },
                    {
                        "name": "🪙 Token Pair",
                        "value": f"**Token A:** `{token0[:6]}...{token0[-4:]}`\n**Token B:** `{token1[:6]}...{token1[-4:]}`",
                        "inline": True
                    },
                    {
                        "name": "💸 Fee Tier",
                        "value": f"**{fee/10000:.2f}%** ({fee} basis points)",
                        "inline": True
                    },
                    {
                        "name": f"{NotificationTemplates.EMOJIS['lightning']} TRADE NOW",
                        "value": (
                            f"[🔥 **INSTANT TRADE**](https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={settings.token_address}) • "
                            f"[📊 Pool Analytics](https://app.uniswap.org/#/pool/{pool_address}) • "
                            f"[🔍 Etherscan](https://etherscan.io/address/{pool_address})"
                        ),
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"Enhanced Pool Listener • {settings.token_symbol} Monitor • Time to trade!",
                    "icon_url": "https://raw.githubusercontent.com/ethereum/ethereum-org-website/dev/src/assets/assets/eth-diamond-purple.png"
                }
            }]
        }
    
    @staticmethod
    def get_email_html(pool_address: str, token0: str, token1: str, fee: int, 
                      liquidity: int, notification_type: str, settings) -> tuple:
        """Create beautiful HTML email"""
        
        if notification_type == "pool_created":
            return NotificationTemplates._get_pool_created_email(
                pool_address, token0, token1, fee, liquidity, settings
            )
        else:  # liquidity_added
            return NotificationTemplates._get_liquidity_added_email(
                pool_address, token0, token1, fee, liquidity, settings
            )
    
    @staticmethod
    def _get_pool_created_email(pool_address: str, token0: str, token1: str, 
                               fee: int, liquidity: int, settings) -> tuple:
        """HTML email for pool creation"""
        
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
        is_tradeable = liquidity >= settings.min_liquidity_threshold
        
        subject = f"🔍 {settings.token_symbol} Pool Discovered - Now Monitoring"
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f8fafc;
                }}
                .container {{
                    background: white;
                    border-radius: 12px;
                    padding: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 30px;
                    border-bottom: 2px solid #e2e8f0;
                }}
                .header h1 {{
                    color: #3498db;
                    font-size: 28px;
                    margin: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                }}
                .status-badge {{
                    background: #3498db;
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: bold;
                    font-size: 14px;
                    display: inline-block;
                    margin: 10px 0;
                }}
                .info-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin: 25px 0;
                }}
                .info-card {{
                    background: #f8fafc;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #3498db;
                }}
                .info-card h3 {{
                    margin: 0 0 10px 0;
                    color: #2c3e50;
                    font-size: 16px;
                }}
                .info-card p {{
                    margin: 0;
                    font-family: monospace;
                    font-size: 14px;
                    background: white;
                    padding: 8px;
                    border-radius: 4px;
                    word-break: break-all;
                }}
                .liquidity-section {{
                    background: {'#d4edda' if is_tradeable else '#fff3cd'};
                    border: 1px solid {'#c3e6cb' if is_tradeable else '#ffeaa7'};
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                    text-align: center;
                }}
                .liquidity-section h3 {{
                    color: {'#155724' if is_tradeable else '#856404'};
                    margin: 0 0 10px 0;
                }}
                .cta-section {{
                    background: #2c3e50;
                    color: white;
                    padding: 25px;
                    border-radius: 8px;
                    text-align: center;
                    margin: 25px 0;
                }}
                .cta-button {{
                    display: inline-block;
                    background: #3498db;
                    color: white;
                    padding: 12px 25px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                    margin: 5px;
                    transition: background 0.3s;
                }}
                .cta-button:hover {{
                    background: #2980b9;
                }}
                .footer {{
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e2e8f0;
                }}
                @media (max-width: 500px) {{
                    .info-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 {settings.token_symbol} Pool Discovered</h1>
                    <div class="status-badge">NOW MONITORING</div>
                    <p style="color: #7f8c8d; margin: 10px 0;">{timestamp}</p>
                </div>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>🎯 Pool Address</h3>
                        <p>{pool_address}</p>
                    </div>
                    <div class="info-card">
                        <h3>💸 Fee Tier</h3>
                        <p>{fee/10000:.2f}% ({fee} basis points)</p>
                    </div>
                    <div class="info-card">
                        <h3>🪙 Token A</h3>
                        <p>{token0}</p>
                    </div>
                    <div class="info-card">
                        <h3>🪙 Token B</h3>
                        <p>{token1}</p>
                    </div>
                </div>
                
                <div class="liquidity-section">
                    <h3>💰 Current Liquidity Status</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 10px 0;">
                        {liquidity:,}
                    </p>
                    <p style="font-size: 16px;">
                        {'🔥 TRADEABLE! Pool has sufficient liquidity.' if is_tradeable else f'⚠️ Below threshold ({settings.min_liquidity_threshold:,}). Will monitor for increases.'}
                    </p>
                </div>
                
                <div class="cta-section">
                    <h3>🔗 Quick Actions</h3>
                    <p style="margin-bottom: 20px;">Ready to explore this pool?</p>
                    <a href="https://etherscan.io/address/{pool_address}" class="cta-button">📊 View on Etherscan</a>
                    <a href="https://app.uniswap.org/#/pool/{pool_address}" class="cta-button">🏊 Uniswap Pool</a>
                    <a href="https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={settings.token_address}" class="cta-button">🔄 Trade Now</a>
                </div>
                
                <div class="footer">
                    <p><strong>Enhanced Pool Listener</strong> • {settings.token_symbol} Monitor</p>
                    <p>Automated crypto pool monitoring with real-time notifications</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return subject, html
    
    @staticmethod
    def _get_liquidity_added_email(pool_address: str, token0: str, token1: str, 
                                  fee: int, liquidity: int, settings) -> tuple:
        """HTML email for liquidity added (tradeable)"""
        
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p UTC")
        
        subject = f"🚀 {settings.token_symbol} NOW TRADEABLE! - High Liquidity Alert"
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    background: white;
                    border-radius: 12px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 30px;
                    border-bottom: 2px solid #e2e8f0;
                }}
                .header h1 {{
                    color: #27ae60;
                    font-size: 32px;
                    margin: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                }}
                .status-badge {{
                    background: linear-gradient(135deg, #00c851, #007e33);
                    color: white;
                    padding: 12px 24px;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 16px;
                    display: inline-block;
                    margin: 15px 0;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    animation: pulse 2s infinite;
                }}
                @keyframes pulse {{
                    0% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.05); }}
                    100% {{ transform: scale(1); }}
                }}
                .alert-banner {{
                    background: linear-gradient(135deg, #ff6b6b, #ee5a52);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    margin: 20px 0;
                    font-size: 18px;
                    font-weight: bold;
                }}
                .liquidity-highlight {{
                    background: linear-gradient(135deg, #4ecdc4, #44a08d);
                    color: white;
                    padding: 30px;
                    border-radius: 12px;
                    text-align: center;
                    margin: 25px 0;
                    box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
                }}
                .liquidity-highlight h3 {{
                    margin: 0 0 15px 0;
                    font-size: 24px;
                }}
                .liquidity-amount {{
                    font-size: 36px;
                    font-weight: bold;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                .info-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin: 25px 0;
                }}
                .info-card {{
                    background: #f8fafc;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #27ae60;
                }}
                .info-card h3 {{
                    margin: 0 0 10px 0;
                    color: #2c3e50;
                    font-size: 16px;
                }}
                .info-card p {{
                    margin: 0;
                    font-family: monospace;
                    font-size: 14px;
                    background: white;
                    padding: 8px;
                    border-radius: 4px;
                    word-break: break-all;
                }}
                .cta-section {{
                    background: linear-gradient(135deg, #2c3e50, #3498db);
                    color: white;
                    padding: 30px;
                    border-radius: 12px;
                    text-align: center;
                    margin: 25px 0;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #e74c3c, #c0392b);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 16px;
                    margin: 8px;
                    transition: all 0.3s;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .cta-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
                }}
                .footer {{
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #e2e8f0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 {settings.token_symbol} TRADEABLE!</h1>
                    <div class="status-badge">🔥 READY TO TRADE 🔥</div>
                    <p style="color: #7f8c8d; margin: 10px 0;">{timestamp}</p>
                </div>
                
                <div class="alert-banner">
                    🏆 TRADING ALERT: {settings.token_symbol} now has sufficient liquidity! 🏆
                </div>
                
                <div class="liquidity-highlight">
                    <h3>💰 Pool Liquidity</h3>
                    <div class="liquidity-amount">{liquidity:,}</div>
                    <p style="margin: 15px 0 0 0; font-size: 16px;">Pool is now actively tradeable!</p>
                </div>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>🎯 Pool Address</h3>
                        <p>{pool_address}</p>
                    </div>
                    <div class="info-card">
                        <h3>💸 Fee Tier</h3>
                        <p>{fee/10000:.2f}% ({fee} basis points)</p>
                    </div>
                    <div class="info-card">
                        <h3>🪙 Token A</h3>
                        <p>{token0}</p>
                    </div>
                    <div class="info-card">
                        <h3>🪙 Token B</h3>
                        <p>{token1}</p>
                    </div>
                </div>
                
                <div class="cta-section">
                    <h3>⚡ TRADE NOW - DON'T MISS OUT!</h3>
                    <p style="margin-bottom: 25px; font-size: 18px;">The pool is ready - start trading immediately!</p>
                    <a href="https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={settings.token_address}" class="cta-button">🔥 INSTANT TRADE</a>
                    <a href="https://app.uniswap.org/#/pool/{pool_address}" class="cta-button">📊 Pool Analytics</a>
                    <a href="https://etherscan.io/address/{pool_address}" class="cta-button">🔍 Etherscan</a>
                </div>
                
                <div class="footer">
                    <p><strong>Enhanced Pool Listener</strong> • {settings.token_symbol} Monitor</p>
                    <p>⚡ Ultra-fast crypto pool monitoring with instant notifications</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return subject, html 
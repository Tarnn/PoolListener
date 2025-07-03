"""
Discord Rich Embed Templates
- Professional Discord embeds with proper colors
- Status-based styling and emojis
- Action buttons and structured fields
"""

from datetime import datetime
from typing import Dict, Any

class DiscordTemplates:
    """Discord-specific notification templates"""
    
    # Brand Colors (Professional Trading Theme)
    COLORS = {
        'success': 0x00FF88,      # Bright Green - Trading Success
        'monitoring': 0x3498DB,   # Professional Blue - Monitoring
        'warning': 0xF39C12,      # Amber - Warning
        'error': 0xE74C3C,        # Red - Error
        'info': 0x9B59B6         # Purple - Information
    }
    
    @staticmethod
    def get_pool_created_embed(pool_address: str, token0: str, token1: str, 
                              fee: int, liquidity: int, settings) -> Dict[str, Any]:
        """Rich embed for pool creation"""
        
        timestamp = datetime.now().isoformat()
        is_tradeable = liquidity >= settings.min_liquidity_threshold
        
        return {
            "embeds": [{
                "title": f"🔍 {settings.token_symbol} Pool Discovered",
                "description": f"**New pool found - Now monitoring for liquidity**",
                "color": DiscordTemplates.COLORS['monitoring'],
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
                            f" 🔥 **TRADEABLE!**" if is_tradeable 
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
    def get_liquidity_added_embed(pool_address: str, token0: str, token1: str, 
                                 fee: int, liquidity: int, settings) -> Dict[str, Any]:
        """Rich embed for liquidity added (tradeable)"""
        
        timestamp = datetime.now().isoformat()
        
        return {
            "embeds": [{
                "title": f"🚀 {settings.token_symbol} NOW TRADEABLE!",
                "description": f"**🔥 Pool has sufficient liquidity - Ready to trade! 💎**",
                "color": DiscordTemplates.COLORS['success'],
                "timestamp": timestamp,
                "thumbnail": {
                    "url": "https://raw.githubusercontent.com/Uniswap/assets/master/blockchains/ethereum/assets/0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984/logo.png"
                },
                "fields": [
                    {
                        "name": f"🏆 TRADING ALERT",
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
                        "name": f"⚡ TRADE NOW",
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
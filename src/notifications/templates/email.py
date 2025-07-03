"""
HTML Email Templates
- Responsive HTML design
- Professional styling with gradients
- Mobile-optimized layouts
- Clear call-to-action buttons
"""

from datetime import datetime
from typing import Tuple

class EmailTemplates:
    """HTML Email Templates for Pool Listener"""
    
    @staticmethod
    def get_pool_created_email(pool_address: str, token0: str, token1: str, 
                              fee: int, liquidity: int, settings) -> Tuple[str, str]:
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
                    <h1>🔍 {settings.token_symbol} Pool Discovered</h1>
                    <div class="status-badge">NOW MONITORING</div>
                    <p style="color: #7f8c8d;">{timestamp}</p>
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
                </div>
                
                <div class="liquidity-section">
                    <h3>💰 Current Liquidity: {liquidity:,}</h3>
                    <p>{'🔥 TRADEABLE! Pool has sufficient liquidity.' if is_tradeable else f'⚠️ Below threshold ({settings.min_liquidity_threshold:,}). Will monitor for increases.'}</p>
                </div>
                
                <div class="cta-section">
                    <h3>🔗 Quick Actions</h3>
                    <a href="https://etherscan.io/address/{pool_address}" class="cta-button">📊 Etherscan</a>
                    <a href="https://app.uniswap.org/#/pool/{pool_address}" class="cta-button">🏊 Pool</a>
                    <a href="https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={settings.token_address}" class="cta-button">🔄 Trade</a>
                </div>
                
                <div class="footer">
                    <p><strong>Enhanced Pool Listener</strong> • {settings.token_symbol} Monitor</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return subject, html
    
    @staticmethod
    def get_liquidity_added_email(pool_address: str, token0: str, token1: str, 
                                 fee: int, liquidity: int, settings) -> Tuple[str, str]:
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
                }}
                .header h1 {{
                    color: #27ae60;
                    font-size: 32px;
                    margin: 0;
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
                }}
                .liquidity-highlight {{
                    background: linear-gradient(135deg, #4ecdc4, #44a08d);
                    color: white;
                    padding: 30px;
                    border-radius: 12px;
                    text-align: center;
                    margin: 25px 0;
                }}
                .liquidity-amount {{
                    font-size: 36px;
                    font-weight: bold;
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
                    margin: 8px;
                    text-transform: uppercase;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 {settings.token_symbol} TRADEABLE!</h1>
                    <div class="status-badge">🔥 READY TO TRADE 🔥</div>
                    <p style="color: #7f8c8d;">{timestamp}</p>
                </div>
                
                <div class="liquidity-highlight">
                    <h3>💰 Pool Liquidity</h3>
                    <div class="liquidity-amount">{liquidity:,}</div>
                    <p>Pool is now actively tradeable!</p>
                </div>
                
                <div class="cta-section">
                    <h3>⚡ TRADE NOW - DON'T MISS OUT!</h3>
                    <a href="https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency={settings.token_address}" class="cta-button">🔥 INSTANT TRADE</a>
                    <a href="https://app.uniswap.org/#/pool/{pool_address}" class="cta-button">📊 Analytics</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        return subject, html 
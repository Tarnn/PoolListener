# Enhanced Pool Listener - Complete Setup Guide

This guide covers setting up the **Enhanced Pool Listener** for monitoring WLFI (World Liberty Financial) with production-grade features including database persistence, multi-channel notifications, and real-time dashboard.

## 🎯 System Components

### 🚀 **Pool Listener** (`poolListener.py`)
- **Purpose**: Production-ready monitoring with all advanced features
- **Features**: SQLite database, multi-channel notifications, retry logic, structured logging, Prometheus metrics
- **Setup time**: 10 minutes

### 🎨 **Notification Templates** (`notification_templates.py`)
- **Purpose**: Beautiful notification templates for all channels
- **Features**: Rich Discord embeds, HTML email templates, professional formatting
- **Setup**: Automatic (included with Pool Listener)

### 📈 **Dashboard** (`dashboard.py`)
- **Purpose**: Real-time visualization and analytics
- **Features**: Interactive charts, metrics, data tables, auto-refresh
- **Setup time**: 5 minutes (after Pool Listener setup)

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Git installed  
- [ ] Gmail account with 2FA enabled (for email notifications)
- [ ] Infura account (free tier sufficient for basic monitoring)
- [ ] Discord/Slack webhooks (optional, for multi-channel notifications)
- [ ] Internet connection
- [ ] Command line knowledge

## 🚀 Pool Listener Setup (10 minutes)

### Step 1: Download and Setup
```bash
# Clone the repository
git clone <repository-url>
cd PoolListener

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Get Infura API Key
1. Go to [https://infura.io/](https://infura.io/)
2. Sign up (free)
3. Create new project → "Web3 API" → "Ethereum Mainnet"
4. Copy your **Project ID**

### Step 3: Setup Gmail App Password
1. Enable 2FA: [myaccount.google.com](https://myaccount.google.com) → Security → 2-Step Verification
2. Generate App Password: Security → App passwords → Mail → Other → "WLFI Monitor"
3. Copy the 16-character password

### Step 4: Create Configuration
Create `.env` file:
```env
# Required - Ethereum & Email
INFURA_API_KEY=paste_your_infura_project_id_here
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=your_gmail_address@gmail.com
RECEIVER_EMAIL=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_16_character_app_password

# WLFI Optimization
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=25000
LIQUIDITY_CHECK_INTERVAL=20
POLLING_INTERVAL=10

# Advanced Features
DATABASE_PATH=wlfi_pools.db
METRICS_PORT=8000
MAX_WORKER_THREADS=10
```

### Step 5: Setup Multi-Channel Notifications (Optional)

#### Discord Webhook Setup
1. Discord Server → Server Settings → Integrations → Create Webhook
2. Copy webhook URL: `https://discord.com/api/webhooks/ID/TOKEN`
3. Format: `discord://ID/TOKEN`

#### Slack Webhook Setup  
1. Slack App → Incoming Webhooks → Add to Slack
2. Copy webhook URL
3. Format: `slack://tokenA/tokenB/tokenC/channel`

#### Telegram Bot Setup
1. Message @BotFather → /newbot → Follow instructions
2. Get bot token and chat ID
3. Format: `tgram://bottoken/chatid`

### Step 6: Add Multi-Channel Configuration
Update your `.env` file:
```env
# Basic settings (from Step 4)
INFURA_API_KEY=your_infura_project_id_here
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=your_gmail_address@gmail.com
RECEIVER_EMAIL=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=25000
LIQUIDITY_CHECK_INTERVAL=20
POLLING_INTERVAL=10

# Advanced features
DATABASE_PATH=wlfi_pools.db
METRICS_PORT=8000
MAX_WORKER_THREADS=10

# Multi-channel notifications (customize as needed)
NOTIFICATION_URLS=discord://webhook_id/webhook_token,mailto://backup@gmail.com

# Optional for performance
LOG_LEVEL=INFO
RETRY_ATTEMPTS=3
```

### Step 7: Test Pool Listener
```bash
# Start the enhanced pool listener
python poolListener.py
```

Expected output:
```
2024-01-15 10:30:45 | INFO | Enhanced Pool Listener Starting...
2024-01-15 10:30:45 | INFO | Token: 0x797a7B11f619dfcc9F0F4b8031b391a7d9772270 (WLFI)
2024-01-15 10:30:45 | INFO | Database initialized: wlfi_pools.db
2024-01-15 10:30:45 | INFO | Metrics server started on port 8000
2024-01-15 10:30:45 | INFO | Notification Channels: 2
2024-01-15 10:30:45 | INFO | Starting from block: 21234567
```

## 📈 Dashboard Setup (5 minutes)

### Step 1: Ensure Pool Listener is Running
The dashboard reads data from the SQLite database created by the pool listener.

### Step 2: Start Dashboard
```bash
# Open new terminal (keep pool listener running)
cd PoolListener
source venv/bin/activate  # Activate same environment

# Start dashboard
streamlit run dashboard.py
```

### Step 3: Access Dashboard
- **URL**: http://localhost:8501
- **Features**: Real-time metrics, charts, data tables
- **Auto-refresh**: Every 30 seconds

Dashboard sections:
- **Metrics**: Total pools, tradeable count, notifications sent
- **Charts**: Pool discovery timeline, liquidity distribution  
- **Tables**: Recent pools and notifications
- **Status**: Live system indicators

## 🔧 Configuration Optimization

### Conservative Setup (Lower API usage)
```env
POLLING_INTERVAL=30
LIQUIDITY_CHECK_INTERVAL=60
MIN_LIQUIDITY_THRESHOLD=10000
MAX_WORKER_THREADS=5
```

### Balanced Setup (Recommended for WLFI)
```env
POLLING_INTERVAL=10
LIQUIDITY_CHECK_INTERVAL=20
MIN_LIQUIDITY_THRESHOLD=25000
MAX_WORKER_THREADS=10
```

### High-Speed Setup (More API usage, faster detection)
```env
POLLING_INTERVAL=6
LIQUIDITY_CHECK_INTERVAL=10
MIN_LIQUIDITY_THRESHOLD=50000
MAX_WORKER_THREADS=20
```

### Enterprise Setup (Maximum performance)
```env
POLLING_INTERVAL=5
LIQUIDITY_CHECK_INTERVAL=8
MIN_LIQUIDITY_THRESHOLD=100000
MAX_WORKER_THREADS=30
LOG_LEVEL=WARNING
RETRY_ATTEMPTS=5
```

## 🧪 Testing Your Setup

### Test 1: Configuration Validation
```bash
# Test configuration loading
python -c "
from poolListener import load_settings
settings = load_settings()
print(f'✅ Configuration valid')
print(f'   Token: {settings.token_address} ({settings.token_symbol})')
print(f'   Threshold: {settings.min_liquidity_threshold:,}')
print(f'   Channels: {len(settings.notification_urls.split(\",\")) if settings.notification_urls else 1}')
"
```

### Test 2: Database Connection
```bash
# Check if database is created and accessible
python -c "
from poolListener import DatabaseManager
db = DatabaseManager('test_pools.db')
stats = db.get_stats()
print(f'✅ Database working: {stats}')
"
```

### Test 3: Notification Channels
```bash
# Test Discord notification
python test_discord_webhook.py

# Test multiple notification channels
python test_both_notifications.py
```

### Test 4: Metrics Endpoint
```bash
# Test Prometheus metrics (while pool listener is running)
curl http://localhost:8000/metrics | head -10
```

### Test 5: Web3 Connection
```bash
# Test Ethereum connection
python -c "
from poolListener import create_web3_connection
w3 = create_web3_connection()
print(f'✅ Connected to Ethereum: Block {w3.eth.block_number}')
"
```

## 🔄 Production Deployment

### Run in Background
```bash
# Run pool listener in background with logging
nohup python poolListener.py > logs/wlfi_$(date +%Y%m%d).log 2>&1 &

# Start dashboard in background
nohup streamlit run dashboard.py > logs/dashboard_$(date +%Y%m%d).log 2>&1 &

# Monitor logs
tail -f logs/wlfi_*.log
```

### Multiple Token Monitoring
```bash
# Different tokens, different configurations
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270 TOKEN_SYMBOL=WLFI DATABASE_PATH=wlfi.db python poolListener.py &

TOKEN_ADDRESS=0x1234567890abcdef1234567890abcdef12345678 TOKEN_SYMBOL=OTHER DATABASE_PATH=other.db python poolListener.py &
```

### System Service (Linux)
Create `/etc/systemd/system/wlfi-monitor.service`:
```ini
[Unit]
Description=WLFI Pool Listener
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/PoolListener
Environment=PATH=/path/to/PoolListener/venv/bin
ExecStart=/path/to/PoolListener/venv/bin/python poolListener.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable wlfi-monitor
sudo systemctl start wlfi-monitor
sudo systemctl status wlfi-monitor
```

## 📊 What to Expect

### Pool Listener Behavior
- **Console Output**: Structured, colored logs with timestamps
- **Pool Created**: Multi-channel notifications + database entry
- **Liquidity Added**: All channels alert when threshold crossed
- **Metrics**: Available at http://localhost:8000/metrics
- **Database**: Historical data stored in SQLite

### Notification Examples

#### Discord Rich Embed
```
🔍 WLFI Pool Discovered
New pool found - Now monitoring for liquidity

🎯 Pool Address: 0xabc123...
🪙 Token Pair: Token A: 0x797a...770 / Token B: 0xC02a...6cC
💸 Fee Tier: 0.30% (3000 basis points)
💰 Current Liquidity: 45,230 🔥 TRADEABLE!
🔗 Quick Actions: [View on Etherscan] • [Uniswap Pool] • [Trade Now]
```

#### HTML Email
```
Subject: 🚀 WLFI NOW TRADEABLE - Liquidity Added!

Beautiful HTML email with:
- Professional styling and typography
- Key information highlighted
- Direct action buttons
- Mobile-responsive design
```

### Dashboard Features
- **Real-time Updates**: Every 30 seconds
- **Visual Charts**: Pool discovery trends, liquidity distribution
- **Data Tables**: Recent pools and notifications with details
- **Status Indicators**: System health and performance metrics

## 🎯 Optimizing for WLFI

### Recommended Settings for WLFI Launch
```env
# Aggressive monitoring for launch day
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=50000
POLLING_INTERVAL=6
LIQUIDITY_CHECK_INTERVAL=10
MAX_WORKER_THREADS=15

# Multiple notification channels for redundancy
NOTIFICATION_URLS=discord://primary/webhook,discord://backup/webhook,slack://team/channel,mailto://emergency@company.com
```

### API Usage Calculation
```
Daily API calls = (86400 / POLLING_INTERVAL) + (discovered_pools × 86400 / LIQUIDITY_CHECK_INTERVAL)

Example (aggressive settings, 2 WLFI pools):
= (86400 / 6) + (2 × 86400 / 10)
= 14,400 + 17,280
= 31,680 calls/day

Infura free tier: 100,000 requests/day ✅
```

## 🚨 Troubleshooting Quick Fixes

### "ImportError: No module named..."
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### "Database locked" error
```bash
# Stop all instances, then restart
pkill -f poolListener
python poolListener.py
```

### Dashboard not loading data
```bash
# Ensure pool listener created database
ls -la wlfi_pools.db
# Should show recent timestamp

# Check database contents
python -c "
from poolListener import DatabaseManager
db = DatabaseManager('wlfi_pools.db')
print(db.get_stats())
"
```

### Metrics endpoint not accessible
```bash
# Check if port is available
netstat -tulpn | grep 8000
# Change METRICS_PORT in .env if needed
```

### Notifications not sending
```bash
# Test individual channels
python test_discord_webhook.py

# Check notification configuration
python -c "
from poolListener import load_settings
settings = load_settings()
print(f'Notification URLs: {settings.notification_urls}')
"
```

## 🔧 Advanced Configuration

### Custom Database Location
```env
DATABASE_PATH=/path/to/custom/location/pools.db
```

### Custom Logging
```env
LOG_LEVEL=DEBUG  # For detailed debugging
LOG_LEVEL=WARNING  # For production (less verbose)
```

### Performance Tuning
```env
# For high-traffic monitoring
MAX_WORKER_THREADS=25
RETRY_ATTEMPTS=5
POLLING_INTERVAL=5
LIQUIDITY_CHECK_INTERVAL=8
```

### Custom Notification Templates
Modify `notification_templates.py` to customize:
- Discord embed colors and formatting
- HTML email templates
- Message content and branding

## 📞 Next Steps

### After Setup
1. **Monitor console output** for first few hours
2. **Check email delivery** and notification channels
3. **Verify dashboard data** is updating
4. **Monitor API usage** on Infura dashboard
5. **Optimize settings** based on performance

### When WLFI Launches
1. **Monitor all channels** for notifications
2. **Check dashboard** for real-time metrics
3. **Verify trading links** work correctly
4. **Act quickly** on notifications
5. **Review historical data** post-launch

### System Monitoring
- **Metrics**: http://localhost:8000/metrics
- **Dashboard**: http://localhost:8501
- **Logs**: Console output or log files
- **Database**: SQLite browser for historical data

---

**🎉 Congratulations!** Your Enhanced Pool Listener is ready to detect when WLFI becomes tradeable with:
- ✅ **Production-grade monitoring** with database persistence
- ✅ **Beautiful multi-channel notifications** (Discord, Email, Slack, Telegram)
- ✅ **Real-time dashboard** for visual monitoring
- ✅ **Enterprise reliability** with retry logic and metrics
- ✅ **Professional presentation** with rich embeds and HTML emails

**Quick Start Commands:**
- **Pool Listener**: `python poolListener.py`
- **Dashboard**: `streamlit run dashboard.py`
- **Metrics**: `curl http://localhost:8000/metrics`
- **Test**: `python test_pool_listener.py` 
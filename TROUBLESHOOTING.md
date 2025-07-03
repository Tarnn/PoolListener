# Enhanced Pool Listener - Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the **Enhanced Pool Listener** system, including the Pool Listener, Notification Templates, and Dashboard components.

## 🎯 System Overview

The Enhanced Pool Listener consists of:
- **🚀 Pool Listener** (`poolListener.py`) - Main monitoring engine with all advanced features
- **🎨 Notification Templates** (`notification_templates.py`) - Beautiful templates for all channels
- **📈 Dashboard** (`dashboard.py`) - Real-time visualization interface

## 🔧 Quick Diagnostic Commands

### System Health Check
```bash
# Check if Pool Listener configuration is valid
python -c "from poolListener import load_settings; print('✅ Configuration valid')"

# Test database connection
python -c "from poolListener import DatabaseManager; db = DatabaseManager('pool_listener.db'); print(f'📊 Database: {db.get_stats()}')"

# Check Web3 connection
python -c "from poolListener import create_web3_connection; w3 = create_web3_connection(); print(f'✅ Ethereum: Block {w3.eth.block_number}')"

# Test notification channels
python test_both_notifications.py

# Check metrics endpoint (if Pool Listener is running)
curl -s http://localhost:8000/metrics | head -10

# Check dashboard accessibility (if running)
curl -s http://localhost:8501 | grep -q "Enhanced Pool Listener" && echo "✅ Dashboard accessible" || echo "❌ Dashboard not accessible"
```

## 🚨 Common Issues and Solutions

### Installation and Setup Issues

#### "ImportError: No module named..."
**Problem**: Missing dependencies after installation

**Solution**:
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade

# If still having issues, recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Verification**:
```bash
python -c "import web3, tenacity, structlog, apprise, pydantic; print('✅ All imports successful')"
```

#### "python: command not found"
**Problem**: Python not installed or not in PATH

**Solution**:
```bash
# Check Python installation
which python3
python3 --version

# Use python3 instead of python if needed
python3 poolListener.py

# Or create alias (add to ~/.bashrc or ~/.zshrc)
alias python=python3
```

### Configuration Issues

#### "Configuration error: missing required fields"
**Problem**: Missing or invalid environment variables

**Diagnosis**:
```bash
# Check which variables are missing
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
required = ['INFURA_API_KEY', 'TOKEN_ADDRESS', 'SENDER_EMAIL', 'RECEIVER_EMAIL', 'EMAIL_PASSWORD']
for var in required:
    value = os.getenv(var)
    print(f'{var}: {\"✅ Set\" if value else \"❌ Missing\"} {\"(\" + value[:10] + \"...)\" if value else \"\"}')
"
```

**Solution**:
```bash
# Create or update .env file with all required variables
cat > .env << 'EOF'
INFURA_API_KEY=your_infura_project_id_here
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=25000
LIQUIDITY_CHECK_INTERVAL=20
POLLING_INTERVAL=10
EOF
```

#### "Invalid Ethereum address format"
**Problem**: Incorrect TOKEN_ADDRESS format

**Diagnosis**:
```bash
python -c "
address = 'YOUR_TOKEN_ADDRESS_HERE'
if len(address) == 42 and address.startswith('0x'):
    print('✅ Valid format')
else:
    print(f'❌ Invalid format: {len(address)} chars, starts with {address[:2]}')
"
```

**Solution**:
- Ensure address is 42 characters long
- Must start with '0x'
- Use checksummed format from Etherscan
- WLFI address: `0x797a7B11f619dfcc9F0F4b8031b391a7d9772270`

### Database Issues

#### "Database locked" error
**Problem**: Multiple instances trying to access the same database

**Diagnosis**:
```bash
# Check for running instances
ps aux | grep poolListener
lsof pool_listener.db 2>/dev/null || echo "No processes using database"
```

**Solution**:
```bash
# Stop all instances
pkill -f poolListener

# Wait a moment, then restart
sleep 5
python poolListener.py
```

#### "Database file not found" 
**Problem**: Database file deleted or permission issues

**Diagnosis**:
```bash
# Check database file
ls -la pool_listener.db
# Check directory permissions
ls -la $(dirname pool_listener.db)
```

**Solution**:
```bash
# Database will be recreated automatically on restart
python poolListener.py

# Or specify custom location
export DATABASE_PATH="/path/to/custom/location/pools.db"
python poolListener.py
```

#### Database corruption
**Problem**: SQLite database file corrupted

**Diagnosis**:
```bash
# Check database integrity
sqlite3 pool_listener.db "PRAGMA integrity_check;"
```

**Solution**:
```bash
# Backup current database
cp pool_listener.db pool_listener_backup_$(date +%Y%m%d).db

# Try to recover
sqlite3 pool_listener.db ".dump" | sqlite3 pool_listener_recovered.db

# If recovery fails, let system recreate
rm pool_listener.db
python poolListener.py
```

### Email and Notification Issues

#### Email notifications not sending
**Problem**: SMTP authentication or configuration issues

**Diagnosis**:
```bash
# Test email configuration
python -c "
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
try:
    msg = MIMEText('Test message from Pool Listener')
    msg['Subject'] = 'Test Email'
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = os.getenv('RECEIVER_EMAIL')
    
    with smtplib.SMTP(os.getenv('SMTP_SERVER', 'smtp.gmail.com'), int(os.getenv('SMTP_PORT', '587'))) as server:
        server.starttls()
        server.login(os.getenv('SENDER_EMAIL'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)
    print('✅ Email test successful')
except Exception as e:
    print(f'❌ Email test failed: {e}')
"
```

**Solution**:
1. **Enable 2FA on Gmail**: Required for app passwords
2. **Generate app password**: Google Account → Security → App passwords
3. **Use app password**: Copy 16-character password (remove spaces)
4. **Check SMTP settings**: Gmail uses `smtp.gmail.com:587`

#### Discord notifications not working
**Problem**: Invalid webhook URL or Discord server issues

**Diagnosis**:
```bash
# Test Discord webhook
python test_discord_webhook.py

# Manual webhook test
python -c "
import requests
webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'
data = {'content': 'Test message from Pool Listener'}
response = requests.post(webhook_url, json=data)
print(f'Status: {response.status_code}, Response: {response.text}')
"
```

**Solution**:
1. **Recreate webhook**: Discord Server → Settings → Integrations → Create Webhook
2. **Check URL format**: Should be `https://discord.com/api/webhooks/ID/TOKEN`
3. **Update .env**: `NOTIFICATION_URLS=discord://ID/TOKEN`

#### "No notification channels configured"
**Problem**: NOTIFICATION_URLS not set or empty

**Diagnosis**:
```bash
# Check notification configuration
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
urls = os.getenv('NOTIFICATION_URLS', '')
if urls:
    channels = [url.strip() for url in urls.split(',') if url.strip()]
    print(f'✅ {len(channels)} notification channels configured')
    for i, channel in enumerate(channels, 1):
        print(f'  {i}. {channel[:30]}...')
else:
    print('ℹ️  No additional notification channels (email only)')
"
```

**Solution**:
```bash
# Add notification channels to .env
echo "NOTIFICATION_URLS=discord://webhook_id/token,slack://tokens/channel" >> .env
```

### Web3 and Blockchain Issues

#### "Failed to connect to Ethereum mainnet"
**Problem**: Network connectivity or invalid Infura API key

**Diagnosis**:
```bash
# Test Infura connection
python -c "
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('INFURA_API_KEY')
provider_url = f'https://mainnet.infura.io/v3/{api_key}'
w3 = Web3(Web3.HTTPProvider(provider_url))

if w3.is_connected():
    print(f'✅ Connected to Ethereum: Block {w3.eth.block_number}')
else:
    print('❌ Connection failed')
"

# Test Infura API key directly
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  https://mainnet.infura.io/v3/YOUR_INFURA_API_KEY
```

**Solution**:
1. **Check API key**: Verify in Infura dashboard
2. **Check rate limits**: Monitor usage in Infura dashboard
3. **Test connectivity**: `ping mainnet.infura.io`
4. **Try alternative endpoint**: Use different Infura endpoint or provider

#### "Rate limit exceeded"
**Problem**: Too many API calls to Infura

**Diagnosis**:
```bash
# Check current configuration
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

polling = int(os.getenv('POLLING_INTERVAL', 12))
liquidity = int(os.getenv('LIQUIDITY_CHECK_INTERVAL', 30))

daily_polling = 86400 / polling
daily_liquidity = 86400 / liquidity  # Assuming 1 pool
total = daily_polling + daily_liquidity

print(f'📊 Estimated daily API usage:')
print(f'  Polling: {daily_polling:,.0f} calls')
print(f'  Liquidity: {daily_liquidity:,.0f} calls')
print(f'  Total: {total:,.0f} calls/day')
print(f'  Status: {\"✅ Within free tier\" if total < 100000 else \"⚠️ Exceeds free tier\"}')
"
```

**Solution**:
```bash
# Reduce API usage by increasing intervals
cat >> .env << 'EOF'
POLLING_INTERVAL=30
LIQUIDITY_CHECK_INTERVAL=60
MAX_WORKER_THREADS=3
EOF

# Or upgrade Infura plan
```

### Performance Issues

#### High memory usage
**Problem**: System consuming too much RAM

**Diagnosis**:
```bash
# Check process memory usage
ps aux | grep poolListener | awk '{print $4 " " $11}' | sort -n

# Check database size
ls -lh pool_listener.db

# Check log level
grep LOG_LEVEL .env || echo "LOG_LEVEL not set (default: INFO)"
```

**Solution**:
```bash
# Optimize performance settings
cat >> .env << 'EOF'
LOG_LEVEL=WARNING
MAX_WORKER_THREADS=3
EOF

# Clean up old data if needed
sqlite3 pool_listener.db "DELETE FROM notifications WHERE sent_at < datetime('now', '-30 days');"
```

#### Slow liquidity checks
**Problem**: Pool liquidity checks taking too long

**Diagnosis**:
```bash
# Check metrics for timing
curl -s http://localhost:8000/metrics | grep liquidity_checks

# Check thread configuration
grep MAX_WORKER_THREADS .env || echo "Using default worker threads"
```

**Solution**:
```bash
# Increase worker threads
echo "MAX_WORKER_THREADS=10" >> .env

# Or reduce check frequency
echo "LIQUIDITY_CHECK_INTERVAL=45" >> .env
```

### Dashboard Issues

#### Dashboard not loading
**Problem**: Streamlit dashboard not accessible

**Diagnosis**:
```bash
# Check if dashboard is running
ps aux | grep streamlit

# Check port availability
netstat -tulpn | grep 8501

# Test dashboard manually
curl -I http://localhost:8501
```

**Solution**:
```bash
# Restart dashboard
pkill -f streamlit
streamlit run dashboard.py

# Use different port if needed
streamlit run dashboard.py --server.port 8502
```

#### Dashboard shows no data
**Problem**: Dashboard displays empty charts and tables

**Diagnosis**:
```bash
# Check if Pool Listener is running and has created database
ls -la pool_listener.db

# Check database contents
python -c "
from poolListener import DatabaseManager
db = DatabaseManager('pool_listener.db')
stats = db.get_stats()
print(f'Database stats: {stats}')
"

# Check if Pool Listener is actually running
ps aux | grep poolListener
```

**Solution**:
```bash
# Ensure Pool Listener is running first
python poolListener.py &

# Wait for some data to be collected, then start dashboard
sleep 60
streamlit run dashboard.py
```

#### Dashboard refresh issues
**Problem**: Data not updating in dashboard

**Diagnosis**:
```bash
# Check if auto-refresh is working
# Look for refresh indicator in dashboard

# Check database timestamp
sqlite3 pool_listener.db "SELECT datetime(MAX(last_checked), 'localtime') as last_update FROM pools;"
```

**Solution**:
- **Manual refresh**: Use browser refresh (F5)
- **Check auto-refresh**: Look for refresh timer in dashboard
- **Restart dashboard**: `streamlit run dashboard.py --server.runOnSave true`

### Port and Network Issues

#### "Port already in use" error
**Problem**: Metrics or dashboard port conflicts

**Diagnosis**:
```bash
# Check what's using the ports
netstat -tulpn | grep -E "(8000|8501)"
lsof -i :8000
lsof -i :8501
```

**Solution**:
```bash
# Use different ports
echo "METRICS_PORT=8001" >> .env
streamlit run dashboard.py --server.port 8502

# Or kill conflicting processes
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:8501 | xargs kill -9
```

#### Firewall blocking connections
**Problem**: External access to dashboard blocked

**Diagnosis**:
```bash
# Check firewall status
sudo ufw status  # Ubuntu
firewall-cmd --list-all  # CentOS/RHEL

# Test local access
curl -I http://localhost:8501

# Test external access (replace IP)
curl -I http://YOUR_SERVER_IP:8501
```

**Solution**:
```bash
# Open firewall ports (Ubuntu)
sudo ufw allow 8501
sudo ufw allow 8000

# Open firewall ports (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

## 🔧 Advanced Troubleshooting

### Debug Mode
Enable detailed logging for troubleshooting:
```bash
# Add to .env file
echo "LOG_LEVEL=DEBUG" >> .env

# Restart with debug output
python poolListener.py 2>&1 | tee debug.log
```

### Component Testing

#### Test Individual Components
```bash
# Test configuration loading
python -c "from poolListener import load_settings; settings = load_settings(); print('✅ Settings loaded')"

# Test database operations
python -c "
from poolListener import DatabaseManager
db = DatabaseManager('test.db')
print('✅ Database operations working')
"

# Test Web3 connection
python -c "
from poolListener import create_web3_connection
w3 = create_web3_connection()
print(f'✅ Web3 connected: {w3.eth.block_number}')
"

# Test notification system
python -c "
from poolListener import NotificationManager
nm = NotificationManager()
print(f'✅ Notification system: {len(nm.apobj.servers)} channels')
"
```

#### Test Notification Templates
```bash
# Test template rendering
python -c "
from notification_templates import NotificationTemplates
templates = NotificationTemplates()
print('✅ Templates loaded successfully')

# Test Discord embed generation
embed = templates.get_discord_embed(
    '0x1234...', '0xabc...', '0xdef...', 3000, 25000, 'pool_created', 
    type('Settings', (), {'token_symbol': 'WLFI', 'min_liquidity_threshold': 25000, 'token_address': '0x797a7B11f619dfcc9F0F4b8031b391a7d9772270'})()
)
print('✅ Discord embed generation working')
"
```

### Performance Monitoring

#### Real-time Performance
```bash
# Monitor system resources
top -p $(pgrep -f poolListener)

# Monitor API calls (if metrics enabled)
watch -n 5 'curl -s http://localhost:8000/metrics | grep -E "(pools_discovered|notifications_sent|liquidity_checks)"'

# Monitor database growth
watch -n 10 'ls -lh pool_listener.db'
```

#### Log Analysis
```bash
# Real-time log monitoring
tail -f debug.log | grep -E "(ERROR|WARNING|Pool|Notification)"

# Error analysis
grep -i error debug.log | tail -20

# Performance analysis
grep -i "duration\|time\|seconds" debug.log | tail -10
```

## 🛡️ Health Monitoring

### Automated Health Checks
Create `health_check.sh`:
```bash
#!/bin/bash
echo "🔍 Enhanced Pool Listener Health Check"
echo "======================================"

# Check if Pool Listener is running
if pgrep -f poolListener > /dev/null; then
    echo "✅ Pool Listener: Running"
else
    echo "❌ Pool Listener: Not running"
fi

# Check database
if [ -f "pool_listener.db" ]; then
    echo "✅ Database: Exists ($(ls -lh pool_listener.db | awk '{print $5}'))"
else
    echo "❌ Database: Missing"
fi

# Check metrics endpoint
if curl -s http://localhost:8000/metrics > /dev/null 2>&1; then
    echo "✅ Metrics: Accessible"
else
    echo "❌ Metrics: Not accessible"
fi

# Check dashboard
if curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo "✅ Dashboard: Accessible"
else
    echo "⚠️  Dashboard: Not accessible (may not be running)"
fi

# Check last activity
LAST_ACTIVITY=$(sqlite3 pool_listener.db "SELECT datetime(MAX(last_checked), 'localtime') FROM pools;" 2>/dev/null || echo "No data")
echo "📊 Last Activity: $LAST_ACTIVITY"

echo "======================================"
```

Make executable and run:
```bash
chmod +x health_check.sh
./health_check.sh
```

### Automated Recovery Script
Create `auto_recovery.sh`:
```bash
#!/bin/bash
LOG_FILE="/tmp/pool_listener_recovery.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if Pool Listener is running
if ! pgrep -f poolListener > /dev/null; then
    log "Pool Listener not running, starting..."
    cd /path/to/PoolListener
    source venv/bin/activate
    nohup python poolListener.py > logs/recovery_$(date +%Y%m%d_%H%M%S).log 2>&1 &
    log "Pool Listener started"
fi

# Check database corruption
if ! sqlite3 pool_listener.db "PRAGMA integrity_check;" | grep -q "ok"; then
    log "Database corruption detected, backing up and recreating..."
    cp pool_listener.db "pool_listener_corrupted_$(date +%Y%m%d_%H%M%S).db"
    rm pool_listener.db
    log "Database will be recreated on next start"
fi

# Monitor disk space
DISK_USAGE=$(df . | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    log "Disk usage high: ${DISK_USAGE}%, cleaning old logs..."
    find logs/ -name "*.log" -mtime +7 -delete
fi
```

Schedule with cron:
```bash
# Edit crontab
crontab -e

# Add line to check every 5 minutes
*/5 * * * * /path/to/auto_recovery.sh
```

## 📞 Getting Additional Help

### Information to Collect
Before seeking help, gather:

1. **System Information**:
   ```bash
   uname -a
   python --version
   pip list | grep -E "(web3|streamlit|tenacity|apprise)"
   ```

2. **Configuration** (remove sensitive data):
   ```bash
   cat .env | sed 's/=.*/=***HIDDEN***/'
   ```

3. **Error Messages**:
   ```bash
   tail -50 debug.log
   ```

4. **System Status**:
   ```bash
   ./health_check.sh
   ```

### Common Error Patterns

| Error Pattern | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| `ImportError: No module named 'web3'` | Missing dependencies | `pip install -r requirements.txt` |
| `ConnectionError: Failed to connect` | Network/API issues | Check Infura key and internet |
| `database is locked` | Multiple instances | `pkill -f poolListener` |
| `Permission denied` | File permissions | `chmod 644 pool_listener.db` |
| `Port already in use` | Port conflict | Use different port or kill process |
| `Invalid address format` | Wrong token address | Check address format (42 chars, starts with 0x) |

---

**🔧 Most issues can be resolved by checking configuration, restarting components, and verifying network connectivity. Use the diagnostic commands above to quickly identify and fix problems.**

**Emergency Recovery Commands:**
- **Full restart**: `pkill -f poolListener && pkill -f streamlit && python poolListener.py & streamlit run dashboard.py &`
- **Clean slate**: `rm pool_listener.db && python poolListener.py`
- **Test everything**: `python test_pool_listener.py && python test_both_notifications.py` 
# Enhanced Pool Listener - Configuration Guide

This guide explains all configuration options for the **Enhanced Pool Listener** system, including database settings, metrics, multi-channel notifications, and dashboard configuration.

## 📋 Configuration Overview

The Enhanced Pool Listener is a **production-ready system** with comprehensive configuration options:

- **🚀 Pool Listener** (`poolListener.py`) - Main monitoring engine with all advanced features
- **🎨 Notification Templates** (`notification_templates.py`) - Beautiful templates for all channels
- **📈 Dashboard** (`dashboard.py`) - Real-time visualization and analytics

All configuration uses environment variables stored in a `.env` file for security and flexibility.

## 🔧 Core Configuration

### Required Variables

#### `INFURA_API_KEY`
- **Description**: Your Infura project ID for Ethereum mainnet access
- **Format**: 32-character alphanumeric string
- **Example**: `abc123def456789012345678901234567`
- **How to get**: Sign up at [infura.io](https://infura.io), create project, copy Project ID
- **Security**: Keep private, never share or commit to version control

#### `TOKEN_ADDRESS`
- **Description**: Ethereum contract address of the token to monitor
- **Format**: 42-character hex string starting with `0x`
- **WLFI Address**: `0x797a7B11f619dfcc9F0F4b8031b391a7d9772270`
- **Validation**: Must be a valid Ethereum address
- **Note**: Case-insensitive, but commonly written in mixed case (checksum format)

#### `SENDER_EMAIL`
- **Description**: Email address that will send notifications
- **Format**: Valid email address
- **Example**: `notifications@yourcompany.com`
- **Requirements**: Must have SMTP access (Gmail recommended)
- **Note**: Should match the account used for `EMAIL_PASSWORD`

#### `RECEIVER_EMAIL`
- **Description**: Email address(es) that will receive notifications
- **Format**: Single email or comma-separated list
- **Examples**: 
  - Single: `trader@example.com`
  - Multiple: `trader1@example.com,trader2@example.com,alerts@company.com`
- **Limits**: No practical limit on number of recipients
- **Processing**: Each recipient receives individual email copy

#### `EMAIL_PASSWORD`
- **Description**: Password for SMTP authentication
- **Format**: For Gmail, 16-character app-specific password
- **Example**: `abcd efgh ijkl mnop`
- **Security**: Use app-specific passwords, never regular account passwords
- **Note**: Remove all spaces when copying from Gmail

### Core Settings

#### `SMTP_SERVER`
- **Description**: SMTP server hostname for email sending
- **Default**: `smtp.gmail.com`
- **Examples**:
  - Gmail: `smtp.gmail.com`
  - Yahoo: `smtp.mail.yahoo.com`
  - Outlook: `smtp-mail.outlook.com`

#### `SMTP_PORT`
- **Description**: SMTP server port number
- **Default**: `587`
- **Common ports**:
  - 587: STARTTLS (recommended)
  - 465: SSL/TLS
  - 25: Unencrypted (not recommended)

#### `TOKEN_SYMBOL`
- **Description**: Human-readable token symbol for notifications
- **Default**: `TOKEN`
- **WLFI Example**: `WLFI`
- **Usage**: Appears in email subjects and messages

#### `MIN_LIQUIDITY_THRESHOLD`
- **Description**: Minimum liquidity required to consider token "tradeable"
- **Default**: `1000`
- **WLFI Recommended**: `25000` or higher
- **Impact**: Higher values prevent false positives from tiny liquidity amounts

#### `LIQUIDITY_CHECK_INTERVAL`
- **Description**: How often (in seconds) to check existing pools for liquidity changes
- **Default**: `30`
- **Range**: 10-300 seconds recommended
- **Impact**: Lower values = faster detection but more API calls

#### `POLLING_INTERVAL`
- **Description**: How often (in seconds) to check for new pool creation events
- **Default**: `12`
- **Range**: 5-60 seconds recommended
- **Impact**: Lower values = faster new pool detection but more API calls

## 🏗️ Advanced Configuration

### Database Configuration

#### `DATABASE_PATH`
- **Description**: SQLite database file path
- **Default**: `pool_listener.db`
- **Examples**:
  - Default: `pool_listener.db`
  - Custom: `/path/to/custom/pools.db`
  - Token-specific: `wlfi_pools.db`
- **Note**: Database will be created automatically if it doesn't exist

### Threading and Performance

#### `MAX_WORKER_THREADS`
- **Description**: Maximum number of concurrent worker threads for liquidity checks
- **Default**: `5`
- **Range**: 3-50 recommended
- **Impact**: Higher values = faster processing but more resource usage
- **Note**: Optimal value depends on system resources and API limits

### Metrics and Monitoring

#### `METRICS_PORT`
- **Description**: Port for Prometheus metrics server
- **Default**: `8000`
- **Access**: `http://localhost:8000/metrics`
- **Note**: Choose port not in use by other services

#### `LOG_LEVEL`
- **Description**: Logging verbosity level
- **Default**: `INFO`
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Impact**: DEBUG shows all operations, ERROR shows only problems

#### `RETRY_ATTEMPTS`
- **Description**: Number of retry attempts for failed operations
- **Default**: `3`
- **Range**: 1-10 recommended
- **Impact**: Higher values = more resilient but slower failure detection

### Multi-Channel Notifications

#### `NOTIFICATION_URLS`
- **Description**: Additional notification channels using Apprise format
- **Default**: Empty (email only)
- **Format**: Comma-separated list of Apprise URLs
- **Examples**:
  ```env
  # Discord
  NOTIFICATION_URLS=discord://webhook_id/webhook_token
  
  # Multiple channels
  NOTIFICATION_URLS=discord://webhook_id/webhook_token,slack://tokenA/tokenB/tokenC/channel,tgram://bottoken/chatid
  
  # With email backup
  NOTIFICATION_URLS=discord://webhook_id/webhook_token,mailto://backup@gmail.com
  ```

### Supported Notification Channels

| Service | Format | Example |
|---------|--------|---------|
| **Discord** | `discord://webhook_id/webhook_token` | `discord://123456789/abcdef...` |
| **Slack** | `slack://tokenA/tokenB/tokenC/channel` | `slack://xoxb-123/xoxb-456/T123/general` |
| **Telegram** | `tgram://bottoken/chatid` | `tgram://123456:ABC-DEF/123456789` |
| **Email** | `mailto://user:pass@domain.com` | `mailto://user:pass@gmail.com` |
| **Microsoft Teams** | `msteams://webhook_url` | `msteams://outlook.office.com/webhook/...` |
| **Pushover** | `pover://user@token` | `pover://user123@app456` |
| **SMS (Twilio)** | `twilio://account_sid:auth_token@from_no/to_no` | `twilio://AC123:auth@+1234567890/+0987654321` |

## 📊 Configuration Examples

### Basic WLFI Monitoring
```env
# Essential settings for WLFI monitoring
INFURA_API_KEY=your_infura_key_here
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=alerts@yourcompany.com
RECEIVER_EMAIL=trader@email.com
EMAIL_PASSWORD=your_16_char_app_password
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=25000
LIQUIDITY_CHECK_INTERVAL=20
POLLING_INTERVAL=10
```

### Advanced WLFI Monitoring
```env
# All basic settings plus advanced features
INFURA_API_KEY=your_infura_key_here
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=alerts@yourcompany.com
RECEIVER_EMAIL=trader@email.com
EMAIL_PASSWORD=your_16_char_app_password
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=25000
LIQUIDITY_CHECK_INTERVAL=20
POLLING_INTERVAL=10

# Advanced features
DATABASE_PATH=wlfi_pools.db
METRICS_PORT=8000
MAX_WORKER_THREADS=15
LOG_LEVEL=INFO
RETRY_ATTEMPTS=3

# Multi-channel notifications
NOTIFICATION_URLS=discord://123456789/abcdef-ghijkl,slack://xoxb-123/xoxb-456/T123/trading-alerts
```

### Enterprise Production Setup
```env
# Enterprise production configuration
INFURA_API_KEY=your_infura_key_here
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=defi-alerts@company.com
RECEIVER_EMAIL=trading-team@company.com,risk-mgmt@company.com
EMAIL_PASSWORD=your_16_char_app_password
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=50000
LIQUIDITY_CHECK_INTERVAL=15
POLLING_INTERVAL=6
MAX_WORKER_THREADS=25

# Enterprise database and monitoring
DATABASE_PATH=/data/production/wlfi_pools.db
METRICS_PORT=9000
LOG_LEVEL=WARNING
RETRY_ATTEMPTS=5

# Multiple notification channels with redundancy
NOTIFICATION_URLS=discord://webhook1/token1,discord://webhook2/token2,slack://tokens/for/trading,msteams://webhook_url,mailto://backup@company.com
```

## 📈 Performance Optimization

### API Usage Planning

#### Calculation Formula
```
Daily API calls = (86400 / POLLING_INTERVAL) + (discovered_pools × 86400 / LIQUIDITY_CHECK_INTERVAL)
```

#### Usage Scenarios

**Conservative (Low API usage)**
```env
POLLING_INTERVAL=30
LIQUIDITY_CHECK_INTERVAL=60
MAX_WORKER_THREADS=5
```
**Estimated usage**: ~6,000 calls/day (1 pool)

**Balanced (Recommended)**
```env
POLLING_INTERVAL=10
LIQUIDITY_CHECK_INTERVAL=20
MAX_WORKER_THREADS=10
```
**Estimated usage**: ~18,000 calls/day (2 pools)

**High-Speed (Fast detection)**
```env
POLLING_INTERVAL=6
LIQUIDITY_CHECK_INTERVAL=10
MAX_WORKER_THREADS=20
```
**Estimated usage**: ~35,000 calls/day (3 pools)

**Enterprise (Maximum speed)**
```env
POLLING_INTERVAL=5
LIQUIDITY_CHECK_INTERVAL=8
MAX_WORKER_THREADS=50
```
**Estimated usage**: ~60,000 calls/day (5 pools)

### Infura Plan Recommendations

| Usage Level | Daily Calls | Recommended Plan | Cost |
|-------------|-------------|------------------|------|
| **Conservative** | <10,000 | Free Tier | $0 |
| **Balanced** | 10,000-30,000 | Free Tier | $0 |
| **High-Speed** | 30,000-80,000 | Core Plan | $50/month |
| **Enterprise** | 80,000+ | Growth Plan | $200/month |

## 🔧 Configuration Optimization

### Memory Optimization
```env
# Reduce memory usage
MAX_WORKER_THREADS=5
LOG_LEVEL=WARNING
```

### Speed Optimization
```env
# Maximize detection speed
POLLING_INTERVAL=5
LIQUIDITY_CHECK_INTERVAL=8
MAX_WORKER_THREADS=25
```

### Cost Optimization
```env
# Minimize API calls
POLLING_INTERVAL=30
LIQUIDITY_CHECK_INTERVAL=60
MAX_WORKER_THREADS=3
```

### Launch Day Optimization
```env
# Optimized for WLFI launch day
POLLING_INTERVAL=5
LIQUIDITY_CHECK_INTERVAL=10
MIN_LIQUIDITY_THRESHOLD=50000
MAX_WORKER_THREADS=20
RETRY_ATTEMPTS=5
NOTIFICATION_URLS=discord://primary,discord://backup,slack://team,mailto://emergency
```

## 🛡️ Security Configuration

### Email Security
```env
# Use dedicated notification email
SENDER_EMAIL=crypto-alerts@yourdomain.com
RECEIVER_EMAIL=secure-inbox@yourdomain.com

# Use app-specific passwords
EMAIL_PASSWORD=secure_16_char_password
```

### Database Security
```env
# Use secure database location
DATABASE_PATH=/secure/path/to/pools.db

# Set appropriate file permissions
# chmod 600 /secure/path/to/pools.db
```

### Webhook Security
```env
# Use HTTPS webhooks only
NOTIFICATION_URLS=discord://secure_webhook_id/secure_token

# Avoid exposing tokens in logs
LOG_LEVEL=INFO  # Don't use DEBUG in production
```

## 🧪 Configuration Testing

### Test Script
Create `test_config.py`:
```python
#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

def test_configuration():
    """Test pool listener configuration"""
    
    # Test required variables
    required = ['INFURA_API_KEY', 'TOKEN_ADDRESS', 'SENDER_EMAIL', 'RECEIVER_EMAIL', 'EMAIL_PASSWORD']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        print("❌ Configuration incomplete:")
        for var in missing:
            print(f"   Missing: {var}")
        return False
    
    # Test configuration loading
    try:
        from poolListener import load_settings
        settings = load_settings()
        print("✅ Configuration valid")
        print(f"   Token: {settings.token_address} ({settings.token_symbol})")
        print(f"   Threshold: {settings.min_liquidity_threshold:,}")
        print(f"   Database: {settings.database_path}")
        print(f"   Metrics port: {settings.metrics_port}")
        print(f"   Worker threads: {settings.max_worker_threads}")
        print(f"   Notification channels: {len(settings.notification_urls.split(',')) if settings.notification_urls else 0}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def calculate_api_usage():
    """Calculate estimated API usage"""
    polling_interval = int(os.getenv('POLLING_INTERVAL', 12))
    liquidity_interval = int(os.getenv('LIQUIDITY_CHECK_INTERVAL', 30))
    
    daily_polling = 86400 / polling_interval
    daily_liquidity = 86400 / liquidity_interval  # Assuming 1 pool
    total_calls = daily_polling + daily_liquidity
    
    print(f"📊 Estimated daily API usage:")
    print(f"   Polling calls: {daily_polling:,.0f}")
    print(f"   Liquidity calls: {daily_liquidity:,.0f} (1 pool)")
    print(f"   Total: {total_calls:,.0f} calls/day")
    
    if total_calls < 100000:
        print("   ✅ Within Infura free tier")
    else:
        print("   ⚠️  Exceeds free tier, consider paid plan")

if __name__ == "__main__":
    print("🧪 Enhanced Pool Listener Configuration Test")
    print("=" * 50)
    
    config_ok = test_configuration()
    calculate_api_usage()
    
    print("=" * 50)
    if config_ok:
        print("🎉 Configuration ready for deployment!")
    else:
        print("⚠️  Configuration needs attention")
```

Run with: `python test_config.py`

## 🔄 Environment-Specific Configuration

### Development Environment
```env
# .env.development
TOKEN_SYMBOL=WLFI-DEV
MIN_LIQUIDITY_THRESHOLD=1000
POLLING_INTERVAL=30
LIQUIDITY_CHECK_INTERVAL=60
LOG_LEVEL=DEBUG
DATABASE_PATH=dev_pools.db
METRICS_PORT=8000
MAX_WORKER_THREADS=3
```

### Staging Environment
```env
# .env.staging
TOKEN_SYMBOL=WLFI-STAGING
MIN_LIQUIDITY_THRESHOLD=10000
POLLING_INTERVAL=15
LIQUIDITY_CHECK_INTERVAL=30
LOG_LEVEL=INFO
DATABASE_PATH=staging_pools.db
METRICS_PORT=8001
MAX_WORKER_THREADS=5
```

### Production Environment
```env
# .env.production
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=50000
POLLING_INTERVAL=6
LIQUIDITY_CHECK_INTERVAL=15
LOG_LEVEL=WARNING
DATABASE_PATH=/data/production/pools.db
METRICS_PORT=9000
MAX_WORKER_THREADS=25
RETRY_ATTEMPTS=5
```

## 📊 Monitoring Configuration Health

### Configuration Validation
```bash
# Validate configuration
python -c "from poolListener import load_settings; settings = load_settings(); print('✅ Configuration valid')"

# Test database connection
python -c "from poolListener import DatabaseManager; db = DatabaseManager('test.db'); print('✅ Database working')"

# Test notification channels
python test_both_notifications.py
```

### Health Check Commands
```bash
# Check Web3 connection
python -c "from poolListener import create_web3_connection; w3 = create_web3_connection(); print(f'✅ Ethereum connected: Block {w3.eth.block_number}')"

# Check metrics endpoint
curl -s http://localhost:8000/metrics | grep -E "(pools_discovered|notifications_sent)" | head -5

# Check database stats
python -c "from poolListener import DatabaseManager; db = DatabaseManager('pool_listener.db'); print(f'📊 Database stats: {db.get_stats()}')"
```

## 🔧 Troubleshooting Configuration

### Common Issues

#### Invalid Token Address
```bash
# Validate token address format
python -c "
address = '0x797a7B11f619dfcc9F0F4b8031b391a7d9772270'
if len(address) == 42 and address.startswith('0x'):
    print('✅ Valid token address')
else:
    print('❌ Invalid token address format')
"
```

#### Database Permission Issues
```bash
# Check database file permissions
ls -la pool_listener.db

# Fix permissions if needed
chmod 644 pool_listener.db
```

#### Port Conflicts
```bash
# Check if metrics port is available
netstat -tulpn | grep 8000

# Use alternative port if needed
echo "METRICS_PORT=8001" >> .env
```

#### Notification Channel Errors
```bash
# Test specific notification channel
python -c "
import apprise
apobj = apprise.Apprise()
apobj.add('discord://webhook_id/webhook_token')
result = apobj.notify('Configuration test message')
print(f'✅ Notification test: {result}')
"
```

## 📚 Configuration Best Practices

### 1. **Environment Separation**
- Use different `.env` files for dev/staging/production
- Never commit `.env` files to version control
- Use environment-specific token addresses for testing

### 2. **Security First**
- Use app-specific passwords for email
- Secure webhook URLs with HTTPS
- Rotate credentials regularly
- Set appropriate file permissions

### 3. **Performance Tuning**
- Start with conservative settings
- Monitor API usage and adjust accordingly
- Scale up gradually based on requirements
- Use metrics to optimize performance

### 4. **Monitoring Setup**
- Enable metrics collection
- Set up dashboard for visual monitoring
- Configure multiple notification channels
- Regular health checks and validation

### 5. **Backup Strategy**
- Backup database regularly
- Store configuration securely
- Document custom settings
- Test recovery procedures

---

**Configuration is the foundation of reliable WLFI monitoring!** Start with basic settings, test thoroughly, then optimize for your specific performance and reliability requirements.

**Quick Configuration Commands:**
- **Test Config**: `python test_config.py`
- **Validate**: `python -c "from poolListener import load_settings; load_settings()"`
- **Check Database**: `python -c "from poolListener import DatabaseManager; DatabaseManager('test.db')"`
- **Test Notifications**: `python test_both_notifications.py` 
# Enhanced Pool Listener Suite

A **production-ready Python application** that monitors Uniswap V3 for new liquidity pools and provides intelligent, beautiful notifications when tokens become tradeable. Specifically designed for monitoring tokens like **WLFI (World Liberty Financial)**.

## 🏗️ System Architecture

The Enhanced Pool Listener consists of **three main components**:

### 🚀 **Pool Listener** (`poolListener.py`)
- **Purpose**: Production-grade monitoring with all advanced features
- **Features**: SQLite database, multi-channel notifications, retry logic, structured logging, Prometheus metrics, threading, data validation
- **Dependencies**: Full suite including database, metrics, multi-channel notifications
- **Status**: Ready for enterprise deployment

### 🎨 **Notification Templates** (`notification_templates.py`) 
- **Purpose**: Beautiful notification templates for all channels
- **Features**: Rich Discord embeds, HTML email templates, consistent branding
- **Supports**: Discord, Slack, Telegram, Email with professional formatting

### 📈 **Dashboard** (`dashboard.py`)
- **Purpose**: Real-time visualization and analytics
- **Features**: Interactive charts, metrics overview, data tables, auto-refresh
- **Access**: Web interface at http://localhost:8501

## ✨ Key Features

### 🔍 **Smart Pool Discovery**
- Real-time monitoring of Uniswap V3 factory for new pools
- Intelligent filtering for target token involvement
- Immediate liquidity assessment

### 💾 **Database Persistence**
- SQLite database for historical data
- Pool tracking with liquidity changes over time
- Notification history and success tracking

### 📱 **Multi-Channel Notifications**
- **Discord**: Rich embeds with colors, thumbnails, and action buttons
- **Email**: Beautiful HTML templates with professional design
- **Slack/Telegram**: Clean, actionable messages
- **Customizable**: Easy to add new channels via Apprise

### 📊 **Enterprise Monitoring**
- Prometheus metrics for system health
- Structured, colored logging with multiple levels
- Thread pool for concurrent processing
- Automatic retry with exponential backoff

### 🛡️ **Reliability Features**
- Database persistence survives restarts
- Duplicate notification prevention
- Error recovery and retry logic
- 99.9% uptime design

## 🎯 Perfect for WLFI Monitoring

Monitor **WLFI (World Liberty Financial)** with enterprise-grade reliability:
- **Immediate alerts** when WLFI pools are created
- **Beautiful notifications** across multiple channels when WLFI becomes tradeable  
- **Historical tracking** of all pool discoveries and liquidity changes
- **Visual dashboard** for real-time monitoring
- **Professional presentation** with rich embeds and HTML emails

## 📦 Installation & Quick Start

### 1. Setup Environment
```bash
# Clone and setup
git clone <repository-url>
cd PoolListener

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Configure for WLFI
Create `.env` file:
```env
# Required - Ethereum & Email
INFURA_API_KEY=your_infura_project_id_here
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=your_email@gmail.com,backup@gmail.com
EMAIL_PASSWORD=your_app_specific_password

# WLFI Optimization
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=25000
LIQUIDITY_CHECK_INTERVAL=20
POLLING_INTERVAL=10

# Advanced Features (Optional)
DATABASE_PATH=wlfi_pools.db
METRICS_PORT=8000
MAX_WORKER_THREADS=10

# Multi-Channel Notifications (Optional)
NOTIFICATION_URLS=discord://webhook_id/webhook_token,slack://tokens/channel
```

### 3. Start Monitoring
```bash
# Start the enhanced pool listener
python poolListener.py
```

### 4. Launch Dashboard (Optional)
```bash
# In a new terminal (keep pool listener running)
streamlit run dashboard.py
# Access at: http://localhost:8501
```

## 🔧 Dependencies & Libraries

### Core Dependencies
```python
web3>=6.0.0              # Ethereum blockchain interaction
python-dotenv>=1.0.0     # Environment variable management
```

### Advanced Features
```python
# Database & Persistence
sqlite3                  # Built into Python - no additional install needed

# Async Operations & Performance
tenacity>=8.2.0          # Retry logic with exponential backoff
backoff>=2.2.0           # Additional backoff strategies

# Structured Logging & Monitoring  
structlog>=23.1.0        # Structured logging framework
colorama>=0.4.6          # Colored console output
prometheus-client>=0.17.0 # Metrics collection and exposure

# Data Validation & Settings
pydantic>=2.0.0          # Type validation and data models

# Multi-Channel Notifications
apprise>=1.4.0           # Unified notification framework (Discord, Slack, Telegram, etc.)
```

### Dashboard Dependencies
```python
streamlit>=1.25.0        # Web dashboard framework
plotly>=5.15.0           # Interactive data visualization
pandas>=1.5.0            # Data manipulation and analysis
```

### Development & Testing
```python
pytest>=7.4.0           # Testing framework
pytest-asyncio>=0.23.0  # Async testing support
```

## 🚀 Usage Examples

### Standard Monitoring
```bash
# Start with default settings
python poolListener.py
```

Expected output:
```
2024-01-15 10:30:45 | INFO | Enhanced Pool Listener Starting...
2024-01-15 10:30:45 | INFO | Token: 0x797a7B11f619dfcc9F0F4b8031b391a7d9772270 (WLFI)
2024-01-15 10:30:45 | INFO | Database initialized: wlfi_pools.db
2024-01-15 10:30:45 | INFO | Metrics server started on port 8000
2024-01-15 10:30:45 | INFO | Notification Channels: 3
2024-01-15 10:30:45 | INFO | Starting from block: 21234567
```

### With Dashboard
```bash
# Terminal 1: Start pool listener
python poolListener.py

# Terminal 2: Start dashboard  
streamlit run dashboard.py
```

Access dashboard at: `http://localhost:8501`

## 📧 Notification Examples

### Discord Rich Embed
Rich Discord notifications with:
- **Professional colors** and thumbnails
- **Clickable action buttons** for immediate trading
- **Structured fields** with key information
- **Branded footer** with system status

### HTML Email Template
Beautiful email notifications featuring:
- **Professional design** with proper typography
- **Visual hierarchy** highlighting important information
- **Direct action buttons** for immediate trading
- **Mobile-responsive** layout

### Slack/Telegram Messages
Clean, actionable messages with:
- **Key information** formatted for readability
- **Direct trading links** for immediate action
- **Consistent branding** across all channels

## 📊 Monitoring & Metrics

### Built-in Prometheus Metrics
```
# Pool discovery tracking
pools_discovered_total{token_symbol="WLFI"} 3

# Notification delivery monitoring  
notifications_sent_total{notification_type="liquidity_added",channel="discord"} 15

# System performance tracking
liquidity_checks_total{status="success"} 450
notification_latency_seconds 0.234
active_pools_total 5
```

### Metrics Endpoint
```
http://localhost:8000/metrics
```

### Dashboard Analytics
- **Pool Discovery Timeline**: Visual chart of pool creation over time
- **Liquidity Distribution**: Histogram of pool liquidity levels
- **Notification Success Rate**: Delivery success tracking across channels
- **System Health**: Real-time status and performance metrics

## 🎛️ Configuration Options

### Basic Configuration
```env
# Essential settings for WLFI monitoring
INFURA_API_KEY=your_key
TOKEN_ADDRESS=0x797a7B11f619dfcc9F0F4b8031b391a7d9772270
SENDER_EMAIL=alerts@yourcompany.com
RECEIVER_EMAIL=trader@email.com
EMAIL_PASSWORD=app_password
TOKEN_SYMBOL=WLFI
MIN_LIQUIDITY_THRESHOLD=25000
```

### Advanced Configuration
```env
# Performance optimization
POLLING_INTERVAL=6                    # Check for new pools every 6 seconds
LIQUIDITY_CHECK_INTERVAL=15          # Check existing pools every 15 seconds
MAX_WORKER_THREADS=20                # Parallel processing threads

# Database and monitoring
DATABASE_PATH=production_pools.db     # Custom database location
METRICS_PORT=9000                    # Custom metrics port

# Multi-channel notifications
NOTIFICATION_URLS=discord://webhook_id/token,slack://tokens/channel,tgram://bot_token/chat_id
```

## 🔧 Advanced Features

### Thread Pool Processing
- Concurrent liquidity checks for multiple pools
- Configurable worker thread count
- Non-blocking operation for new pool discovery

### Retry Logic & Reliability
- Exponential backoff for failed operations
- Automatic recovery from network issues
- 99.9% uptime design with graceful error handling

### Database Persistence
- SQLite database with proper schema
- Historical tracking of all pools and notifications
- Survives system restarts and maintains state

### Professional Notifications
- Rich Discord embeds with thumbnails and action buttons
- HTML email templates with responsive design
- Consistent branding across all channels

## 🧪 Testing

### Test Suite
```bash
# Run comprehensive tests
python test_pool_listener.py

# Test notification channels
python test_discord_webhook.py
python test_both_notifications.py

# Run all tests
python run_tests.py
```

### Configuration Testing
```bash
# Validate configuration
python -c "from poolListener import load_settings; print('✅ Configuration valid')"

# Test database connection
python -c "from poolListener import DatabaseManager; db = DatabaseManager('test.db'); print('✅ Database working')"
```

## 🔍 Monitoring Best Practices

### For WLFI Launch Day
```env
# Aggressive monitoring settings
POLLING_INTERVAL=5
LIQUIDITY_CHECK_INTERVAL=10  
MIN_LIQUIDITY_THRESHOLD=50000
MAX_WORKER_THREADS=25

# Multiple notification channels
NOTIFICATION_URLS=discord://primary,discord://backup,slack://trading-team,mailto://emergency@company.com
```

### Production Deployment
```env
# Balanced performance and cost
POLLING_INTERVAL=10
LIQUIDITY_CHECK_INTERVAL=20
MIN_LIQUIDITY_THRESHOLD=25000
MAX_WORKER_THREADS=15
```

## 📞 Getting Help

1. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Step-by-step setup instructions
2. **[CONFIGURATION.md](CONFIGURATION.md)** - Complete configuration reference  
3. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
4. **[DOCS.md](DOCS.md)** - Documentation navigation

## 🔐 Security & Privacy

- **Environment variables** for all sensitive configuration
- **App-specific passwords** for email authentication
- **Secure webhook URLs** for Discord/Slack integration
- **Database encryption** options for sensitive data
- **Regular security updates** for all dependencies

## ⚠️ Disclaimer

This software is for educational and informational purposes only. Always verify information independently and understand the risks of cryptocurrency trading.

---

**🚀 Ready to monitor WLFI with enterprise-grade reliability?**

1. **Setup**: Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions
2. **Configure**: Use [CONFIGURATION.md](CONFIGURATION.md) for optimization  
3. **Deploy**: Run `python poolListener.py` and `streamlit run dashboard.py`
4. **Monitor**: Access dashboard at http://localhost:8501 and metrics at :8000/metrics

**You'll be the first to know when WLFI becomes tradeable with beautiful, professional notifications!** 🎯
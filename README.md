# Uniswap V3 Pool Listener

A Python application that monitors the Uniswap V3 factory for new liquidity pools involving any specified token and sends email notifications when such pools are created.

## Features

- 🔍 **Real-time monitoring**: Continuously listens for new Uniswap V3 pool creation events
- 🎯 **Token-specific**: Only triggers alerts for pools involving your specified token
- 📧 **Multiple email notifications**: Sends detailed email alerts to multiple recipients
- 🔄 **Automatic recovery**: Handles connection errors and retries automatically
- ⚡ **Efficient**: Uses event filtering to minimize API calls
- 🔒 **Secure**: Uses environment variables for sensitive configuration
- 💰 **Liquidity verification**: Checks if pools have actual liquidity (tradeable)

## Requirements

- Python 3.7+
- Infura API key (or other Ethereum node provider)
- Gmail account with app-specific password (for email notifications)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PoolListener
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The application uses environment variables for all configuration. You can set these in several ways:

### Method 1: Export Environment Variables
```bash
export INFURA_API_KEY="your_infura_project_id"
export TOKEN_ADDRESS="0x1234567890abcdef1234567890abcdef12345678"
export SENDER_EMAIL="your_email@gmail.com"
export RECEIVER_EMAIL="recipient1@gmail.com,recipient2@gmail.com,recipient3@gmail.com"
export EMAIL_PASSWORD="your_app_specific_password"
```

### Method 2: Create a .env file (recommended)
Create a `.env` file in the project directory:
```env
# Required Configuration
INFURA_API_KEY=your_infura_project_id
TOKEN_ADDRESS=0x1234567890abcdef1234567890abcdef12345678
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=recipient1@gmail.com,recipient2@gmail.com
EMAIL_PASSWORD=your_app_specific_password

# Optional Configuration (with defaults shown)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
POLLING_INTERVAL=12
TOKEN_SYMBOL=TOKEN
```

**Important**: Add `.env` to your `.gitignore` file to avoid committing sensitive information.

### Method 3: Set Variables Before Running
```bash
INFURA_API_KEY="your_key" TOKEN_ADDRESS="0x..." python poolListener.py
```

## Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `INFURA_API_KEY` | Your Infura project ID | `abc123def456...` |
| `TOKEN_ADDRESS` | Target token contract address | `0x1234567890abcdef...` |
| `SENDER_EMAIL` | Email address to send from | `alerts@yourdomain.com` |
| `RECEIVER_EMAIL` | Email addresses to send to (comma-separated) | `user1@email.com,user2@email.com` |
| `EMAIL_PASSWORD` | App-specific password for sender email | `abcd efgh ijkl mnop` |

## Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_SERVER` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `POLLING_INTERVAL` | Seconds between blockchain polls | `12` |
| `TOKEN_SYMBOL` | Token symbol for display in messages | `TOKEN` |

## Getting Required Information

### Infura API Key
1. Go to [Infura](https://infura.io/)
2. Create a free account
3. Create a new project
4. Copy your Project ID (this is your API key)

### Gmail App Password
1. Enable 2-factor authentication on your Gmail account
2. Go to Google Account settings
3. Security → App passwords
4. Generate a new app password for this application

### Token Address
Find your token's contract address from:
- [Etherscan](https://etherscan.io/)
- [CoinGecko](https://coingecko.com/)
- [CoinMarketCap](https://coinmarketcap.com/)
- The token's official website

## Usage

### Using .env file (recommended)
1. Create your `.env` file with the required variables
2. Run the application:
```bash
python poolListener.py
```

### Using environment variables
```bash
# Set your environment variables first, then run:
python poolListener.py
```

The application will:
1. Load configuration from environment variables
2. Connect to Ethereum mainnet via Infura
3. Start monitoring from the latest block
4. Check for new Uniswap V3 pool creation events
5. Send email notifications for any pools involving your target token
6. Continue running until manually stopped (Ctrl+C)

## How It Works

1. **Configuration**: Loads all settings from environment variables with validation
2. **Connection**: Establishes a connection to Ethereum mainnet using Web3 and Infura
3. **Event Monitoring**: Listens for `PoolCreated` events from the Uniswap V3 factory contract
4. **Filtering**: Checks if either token in the new pool matches your target token address
5. **Liquidity Verification**: Checks if the pool has actual liquidity (tradeable)
6. **Notification**: Sends email alerts to all recipients with pool details
7. **Continuous Operation**: Polls for new blocks at configurable intervals

## Email Notification Format

When a new pool is detected involving your target token, all recipients will receive an email with:
- Pool contract address
- Token addresses (token0 and token1)
- Fee tier
- Liquidity status (tradeable or not)
- Direct Etherscan and Uniswap links

## Multiple Recipients

The `RECEIVER_EMAIL` variable supports multiple email addresses separated by commas:
```env
RECEIVER_EMAIL=user1@gmail.com,user2@yahoo.com,alerts@company.com
```

All recipients will receive the same notification when a pool is detected.

## Security Considerations

- **Environment variables**: All sensitive data is stored in environment variables
- **Never commit secrets**: Add `.env` to your `.gitignore` file
- **App-specific passwords**: Use Gmail app-specific passwords instead of your main password
- **Rate limiting**: Be aware of API rate limits on your Infura plan
- **Token verification**: Always verify token addresses from official sources

## Troubleshooting

### Common Issues

1. **Configuration errors**: The app will show exactly which environment variables are missing
2. **Connection failed**: Check your Infura API key and internet connection
3. **Email not sending**: Verify Gmail app password and sender email configuration
4. **No events detected**: Ensure the token address is correct
5. **Rate limit errors**: Consider upgrading your Infura plan or increasing polling interval

### Environment Variable Debugging
```bash
# Check if variables are set
echo $INFURA_API_KEY
echo $TOKEN_ADDRESS
echo $RECEIVER_EMAIL
```

### Logs

The application provides console output for:
- Configuration validation
- Connection status
- Block monitoring progress
- Pool detection events
- Email notification status
- Error messages

## Customization

You can customize the application by modifying environment variables:
- Change `POLLING_INTERVAL` to poll more or less frequently
- Use different `SMTP_SERVER` and `SMTP_PORT` for other email providers
- Monitor different tokens by changing `TOKEN_ADDRESS`
- Add more recipients by updating `RECEIVER_EMAIL`

Advanced customizations require code changes:
- Monitor multiple tokens simultaneously
- Add Discord/Slack notifications
- Store pool data in a database
- Add more detailed analysis of detected pools

## Example .env Template

```env
# Copy this template to .env and fill in your values

# Required - Get from https://infura.io/
INFURA_API_KEY=

# Required - Token contract address you want to monitor
TOKEN_ADDRESS=

# Required - Email configuration
SENDER_EMAIL=
RECEIVER_EMAIL=email1@gmail.com,email2@gmail.com
EMAIL_PASSWORD=

# Optional - SMTP configuration (defaults shown)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587

# Optional - Polling interval in seconds (default: 12)
# POLLING_INTERVAL=12

# Optional - Token symbol for display (default: TOKEN)
# TOKEN_SYMBOL=MYTOKEN
```

## Use Cases

This tool is perfect for:
- 🚀 **New token launches**: Get notified when your token becomes tradeable
- 📊 **DeFi monitoring**: Track when liquidity is added to specific tokens
- 🔍 **Market research**: Monitor when new trading pairs are created
- 📈 **Trading opportunities**: Be first to know when tokens become available
- 🏢 **Business intelligence**: Track competitor token launches

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with environment variables
5. Submit a pull request

## License

This project is open source. Please check the LICENSE file for details.

## Disclaimer

This software is provided as-is for educational and informational purposes. Always verify pool information independently before making any trading decisions. The developers are not responsible for any financial losses incurred from using this software. 
# WLFI Pool Listener

A Python application that monitors the Uniswap V3 factory for new liquidity pools involving the WLFI token and sends email notifications when such pools are created.

## Features

- 🔍 **Real-time monitoring**: Continuously listens for new Uniswap V3 pool creation events
- 🎯 **WLFI-specific**: Only triggers alerts for pools involving the WLFI token
- 📧 **Email notifications**: Sends detailed email alerts when new pools are detected
- 🔄 **Automatic recovery**: Handles connection errors and retries automatically
- ⚡ **Efficient**: Uses event filtering to minimize API calls
- 🔒 **Secure**: Uses environment variables for sensitive configuration

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
export WLFI_ADDRESS="0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6"
export SENDER_EMAIL="your_email@gmail.com"
export RECEIVER_EMAIL="recipient@gmail.com"
export EMAIL_PASSWORD="your_app_specific_password"
```

### Method 2: Create a .env file (recommended)
Create a `.env` file in the project directory:
```env
# Required Configuration
INFURA_API_KEY=your_infura_project_id
WLFI_ADDRESS=0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=recipient@gmail.com
EMAIL_PASSWORD=your_app_specific_password

# Optional Configuration (with defaults shown)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
POLLING_INTERVAL=12
```

**Important**: Add `.env` to your `.gitignore` file.

### Method 3: Set Variables Before Running
```bash
INFURA_API_KEY="your_key" WLFI_ADDRESS="0x..." python poolListener.py
```

## Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `INFURA_API_KEY` | Your Infura project ID | `abc123def456...` |
| `WLFI_ADDRESS` | WLFI token contract address | `0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6` |
| `SENDER_EMAIL` | Email address to send from | `alerts@yourdomain.com` |
| `RECEIVER_EMAIL` | Email address to send to | `you@email.com` |
| `EMAIL_PASSWORD` | App-specific password for sender email | `abcd efgh ijkl mnop` |

## Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMTP_SERVER` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `POLLING_INTERVAL` | Seconds between blockchain polls | `12` |

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

### WLFI Token Address
The WLFI token address is: `0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6`
You can verify this on [Etherscan](https://etherscan.io/token/0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6)

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
5. Send email notifications for any pools involving WLFI
6. Continue running until manually stopped (Ctrl+C)

## How It Works

1. **Configuration**: Loads all settings from environment variables with validation
2. **Connection**: Establishes a connection to Ethereum mainnet using Web3 and Infura
3. **Event Monitoring**: Listens for `PoolCreated` events from the Uniswap V3 factory contract
4. **Filtering**: Checks if either token in the new pool matches the WLFI address
5. **Notification**: Sends email alerts with pool details when a match is found
6. **Continuous Operation**: Polls for new blocks at configurable intervals

## Email Notification Format

When a new WLFI pool is detected, you'll receive an email with:
- Pool contract address
- Token addresses (token0 and token1)
- Fee tier
- Block information

## Security Considerations

- **Environment variables**: All sensitive data is stored in environment variables
- **Never commit secrets**: Add `.env` to your `.gitignore` file
- **App-specific passwords**: Use Gmail app-specific passwords instead of your main password
- **Rate limiting**: Be aware of API rate limits on your Infura plan
- **Token verification**: Always verify the WLFI token address from official sources

## Troubleshooting

### Common Issues

1. **Configuration errors**: The app will show exactly which environment variables are missing
2. **Connection failed**: Check your Infura API key and internet connection
3. **Email not sending**: Verify Gmail app password and sender email configuration
4. **No events detected**: Ensure the WLFI token address is correct
5. **Rate limit errors**: Consider upgrading your Infura plan or increasing polling interval

### Environment Variable Debugging
```bash
# Check if variables are set
echo $INFURA_API_KEY
echo $WLFI_ADDRESS
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
- Monitor different tokens by changing `WLFI_ADDRESS`

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

# Required - WLFI token contract address
WLFI_ADDRESS=0xdA5e1988097297dCdc1f90D4dFE7909e847CBeF6

# Required - Email configuration
SENDER_EMAIL=
RECEIVER_EMAIL=
EMAIL_PASSWORD=

# Optional - SMTP configuration (defaults shown)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587

# Optional - Polling interval in seconds (default: 12)
# POLLING_INTERVAL=12
```

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
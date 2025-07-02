from web3 import Web3
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Web3 setup
# Replace 'YOUR_INFURA_KEY' with your actual Infura API key
infura_url = 'https://mainnet.infura.io/v3/YOUR_INFURA_KEY'
w3 = Web3(Web3.HTTPProvider(infura_url))

# Verify connection to Ethereum mainnet
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum mainnet. Check your Infura URL or API key.")

# Uniswap V3 Factory contract details
factory_address = '0x1F98431c8aD98523631AE4a59f267346ea31F984'  # Uniswap V3 factory address
# Minimal ABI for the "PoolCreated" event
factory_abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "token0", "type": "address"},
            {"indexed": True, "name": "token1", "type": "address"},
            {"indexed": True, "name": "fee", "type": "uint24"},
            {"name": "tickSpacing", "type": "int24"},
            {"name": "pool", "type": "address"}
        ],
        "name": "PoolCreated",
        "type": "event"
    }
]
contract = w3.eth.contract(address=factory_address, abi=factory_abi)

# WLFI token address (replace with the actual WLFI token contract address)
wlfi_address = '0x...'  # TODO: Replace with the actual WLFI token address

# Email configuration
sender_email = 'your_email@example.com'    # Replace with your email address
receiver_email = 'recipient@example.com'   # Replace with the recipient's email address
password = 'your_password'                 # Replace with your email password or app-specific password

# Function to send email notification
def send_email(pool_address, token0, token1, fee):
    """Send an email notification when a new pool involving WLFI is detected."""
    subject = "New Uniswap V3 Pool Created with WLFI"
    body = f"A new Uniswap V3 pool has been created involving WLFI:\n" \
           f"Pool address: {pool_address}\n" \
           f"Tokens: {token0} and {token1}\n" \
           f"Fee: {fee}"
    
    # Create email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587

from web3 import Web3
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
def get_required_env(var_name):
    """Get required environment variable or raise an error."""
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Required environment variable '{var_name}' is not set")
    return value

def get_optional_env(var_name, default_value):
    """Get optional environment variable with default value."""
    return os.getenv(var_name, default_value)

# Load configuration
try:
    INFURA_API_KEY = get_required_env('INFURA_API_KEY')
    WLFI_ADDRESS = get_required_env('WLFI_ADDRESS')
    SENDER_EMAIL = get_required_env('SENDER_EMAIL')
    RECEIVER_EMAIL = get_required_env('RECEIVER_EMAIL')
    EMAIL_PASSWORD = get_required_env('EMAIL_PASSWORD')
    
    # Optional configurations with defaults
    SMTP_SERVER = get_optional_env('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(get_optional_env('SMTP_PORT', '587'))
    POLLING_INTERVAL = int(get_optional_env('POLLING_INTERVAL', '12'))
    
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("\nPlease set the required environment variables:")
    print("- INFURA_API_KEY: Your Infura project ID")
    print("- WLFI_ADDRESS: WLFI token contract address")
    print("- SENDER_EMAIL: Your email address")
    print("- RECEIVER_EMAIL: Recipient email address")
    print("- EMAIL_PASSWORD: Your email app-specific password")
    print("\nOptional environment variables:")
    print("- SMTP_SERVER: SMTP server (default: smtp.gmail.com)")
    print("- SMTP_PORT: SMTP port (default: 587)")
    print("- POLLING_INTERVAL: Seconds between polls (default: 12)")
    exit(1)

# Web3 setup
infura_url = f'https://mainnet.infura.io/v3/{INFURA_API_KEY}'
w3 = Web3(Web3.HTTPProvider(infura_url))

# Verify connection to Ethereum mainnet
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum mainnet. Check your Infura API key or internet connection.")

print(f"✅ Successfully connected to Ethereum mainnet")
print(f"📡 Using Infura endpoint: {infura_url}")

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

# Email configuration
sender_email = SENDER_EMAIL
receiver_email = RECEIVER_EMAIL
password = EMAIL_PASSWORD

# Function to check if a pool has liquidity
def check_pool_liquidity(pool_address):
    """Check if a pool has meaningful liquidity."""
    try:
        # Minimal pool ABI to get liquidity
        pool_abi = [
            {
                "inputs": [],
                "name": "liquidity",
                "outputs": [{"internalType": "uint128", "name": "", "type": "uint128"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "token0",
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "token1", 
                "outputs": [{"internalType": "address", "name": "", "type": "address"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        pool_contract = w3.eth.contract(address=pool_address, abi=pool_abi)
        liquidity = pool_contract.functions.liquidity().call()
        
        # Consider pool tradeable if liquidity > 0
        return liquidity > 0, liquidity
    except Exception as e:
        print(f"Error checking pool liquidity: {e}")
        return False, 0

# Enhanced function to send email notification with liquidity info
def send_email(pool_address, token0, token1, fee, liquidity=None):
    """Send an email notification when a new pool involving WLFI is detected."""
    subject = "🚨 WLFI Pool Created - Token May Be Tradeable!"
    
    liquidity_info = ""
    if liquidity is not None:
        if liquidity > 0:
            liquidity_info = f"\n💰 Pool Liquidity: {liquidity} (TRADEABLE!)"
        else:
            liquidity_info = f"\n⚠️  Pool Liquidity: {liquidity} (NO LIQUIDITY YET)"
    
    body = f"🎉 A new Uniswap V3 pool has been created involving WLFI!\n\n" \
           f"📍 Pool address: {pool_address}\n" \
           f"🪙 Token0: {token0}\n" \
           f"🪙 Token1: {token1}\n" \
           f"💸 Fee: {fee} basis points\n" \
           f"{liquidity_info}\n\n" \
           f"🔗 View on Etherscan: https://etherscan.io/address/{pool_address}\n" \
           f"📊 Check on Uniswap: https://app.uniswap.org/#/pool/{pool_address}"
    
    # Create email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS encryption
            server.login(sender_email, password)
            server.send_message(message)
        print(f"✅ Email notification sent successfully for pool: {pool_address}")
    except Exception as e:
        print(f"❌ Failed to send email notification: {e}")

# Function to check if a pool involves WLFI token
def involves_wlfi(token0, token1):
    """Check if either token in the pool is WLFI."""
    return token0.lower() == WLFI_ADDRESS.lower() or token1.lower() == WLFI_ADDRESS.lower()

# Main event listener function
def listen_for_pools():
    """Listen for new Uniswap V3 pool creation events involving WLFI."""
    print("Starting WLFI pool listener...")
    print(f"Monitoring for pools involving WLFI token: {WLFI_ADDRESS}")
    
    # Get the latest block number to start listening from
    latest_block = w3.eth.get_block('latest')['number']
    print(f"Starting from block: {latest_block}")
    
    while True:
        try:
            # Get new blocks and check for PoolCreated events
            current_block = w3.eth.get_block('latest')['number']
            
            if current_block > latest_block:
                # Create event filter for new blocks
                event_filter = contract.events.PoolCreated.create_filter(
                    fromBlock=latest_block + 1,
                    toBlock=current_block
                )
                
                # Get all events in the range
                events = event_filter.get_all_entries()
                
                for event in events:
                    token0 = event['args']['token0']
                    token1 = event['args']['token1']
                    fee = event['args']['fee']
                    pool_address = event['args']['pool']
                    
                    # Check if this pool involves WLFI
                    if involves_wlfi(token0, token1):
                        print(f"\n🎉 NEW WLFI POOL DETECTED!")
                        print(f"📍 Pool address: {pool_address}")
                        print(f"🪙 Token0: {token0}")
                        print(f"🪙 Token1: {token1}")
                        print(f"💸 Fee: {fee} basis points")
                        print(f"🔗 Etherscan: https://etherscan.io/address/{pool_address}")
                        
                        # Check pool liquidity
                        print("⏳ Checking pool liquidity...")
                        has_liquidity, liquidity_amount = check_pool_liquidity(pool_address)
                        
                        if has_liquidity:
                            print(f"💰 POOL HAS LIQUIDITY: {liquidity_amount} - WLFI IS LIKELY TRADEABLE! 🚀")
                        else:
                            print(f"⚠️  Pool has no liquidity yet: {liquidity_amount}")
                        
                        # Send email notification
                        send_email(pool_address, token0, token1, fee, liquidity_amount)
                        print("📧 Email notification sent!")
                        print("-" * 60)
                
                latest_block = current_block
            
            # Wait 12 seconds (approximate Ethereum block time)
            time.sleep(POLLING_INTERVAL)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(30)  # Wait 30 seconds before retrying

if __name__ == "__main__":
    try:
        listen_for_pools()
    except KeyboardInterrupt:
        print("\nShutting down pool listener...")
    except Exception as e:
        print(f"Fatal error: {e}")

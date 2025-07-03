"""
Configuration Management
- Type-safe settings with Pydantic V2
- Environment variable validation
- Default values and validation rules
"""

import os
from typing import List
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    """Type-safe configuration with validation"""
    
    # Required Blockchain Settings
    infura_api_key: str
    token_address: str
    
    # Required Email Settings  
    sender_email: str
    receiver_email: str
    email_password: str
    
    # Optional Email Settings
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    
    # Token Monitoring Settings
    token_symbol: str = "TOKEN"
    polling_interval: int = 12
    min_liquidity_threshold: int = 1000
    liquidity_check_interval: int = 30
    
    # System Settings
    database_path: str = "pool_listener.db"
    metrics_port: int = 8000
    max_worker_threads: int = 5
    log_level: str = "INFO"
    
    # Notification Channels (apprise format)
    notification_urls: str = ""
    
    @field_validator('token_address')
    @classmethod
    def validate_token_address(cls, v):
        if not v or not v.startswith('0x') or len(v) != 42:
            raise ValueError('Invalid Ethereum address format')
        return v.lower()
    
    @field_validator('infura_api_key')
    @classmethod
    def validate_infura_key(cls, v):
        if not v or len(v) < 20:
            raise ValueError('Invalid Infura API key')
        return v
    
    @property
    def receiver_emails(self) -> List[str]:
        return [email.strip() for email in self.receiver_email.split(',')]
    
    @property
    def infura_url(self) -> str:
        return f"https://mainnet.infura.io/v3/{self.infura_api_key}"

def load_settings() -> Settings:
    """Load and validate settings from environment"""
    try:
        return Settings(
            infura_api_key=os.getenv('INFURA_API_KEY'),
            token_address=os.getenv('TOKEN_ADDRESS'),
            sender_email=os.getenv('SENDER_EMAIL'),
            receiver_email=os.getenv('RECEIVER_EMAIL'),
            email_password=os.getenv('EMAIL_PASSWORD'),
            smtp_server=os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            smtp_port=int(os.getenv('SMTP_PORT', '587')),
            polling_interval=int(os.getenv('POLLING_INTERVAL', '12')),
            token_symbol=os.getenv('TOKEN_SYMBOL', 'TOKEN'),
            min_liquidity_threshold=int(os.getenv('MIN_LIQUIDITY_THRESHOLD', '1000')),
            liquidity_check_interval=int(os.getenv('LIQUIDITY_CHECK_INTERVAL', '30')),
            database_path=os.getenv('DATABASE_PATH', 'pool_listener.db'),
            metrics_port=int(os.getenv('METRICS_PORT', '8000')),
            max_worker_threads=int(os.getenv('MAX_WORKER_THREADS', '5')),
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            notification_urls=os.getenv('NOTIFICATION_URLS', '')
        )
    except Exception as e:
        raise ValueError(f"Configuration error: {e}") 
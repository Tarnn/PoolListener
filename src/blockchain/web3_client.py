"""
Web3 Client
- Connection management with retry logic
- Pool liquidity checking
- Event filtering and processing
"""

import time
from typing import Tuple
from web3 import Web3
from web3.exceptions import Web3Exception
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger(__name__)

class Web3Client:
    """Web3 client with retry logic and connection management"""
    
    def __init__(self, infura_url: str):
        self.infura_url = infura_url
        self.w3 = self._create_connection()
        self.uniswap_factory_address = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        self.uniswap_factory_abi = [
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "token0", "type": "address"},
                    {"indexed": True, "name": "token1", "type": "address"},
                    {"indexed": True, "name": "fee", "type": "uint24"},
                    {"indexed": False, "name": "tickSpacing", "type": "int24"},
                    {"indexed": False, "name": "pool", "type": "address"}
                ],
                "name": "PoolCreated",
                "type": "event"
            }
        ]
        self.pool_abi = [
            {
                "inputs": [],
                "name": "liquidity",
                "outputs": [{"name": "", "type": "uint128"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        self.contract = self.w3.eth.contract(
            address=self.uniswap_factory_address,
            abi=self.uniswap_factory_abi
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Web3Exception, ConnectionError))
    )
    def _create_connection(self) -> Web3:
        """Create Web3 connection with retry logic"""
        try:
            w3 = Web3(Web3.HTTPProvider(self.infura_url))
            
            if not w3.is_connected():
                raise ConnectionError("Failed to connect to Ethereum node")
            
            logger.info("✅ Connected to Ethereum mainnet")
            return w3
            
        except Exception as e:
            logger.error(f"❌ Web3 connection failed: {e}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type((Web3Exception, ConnectionError))
    )
    def check_pool_liquidity(self, pool_address: str, min_threshold: int) -> Tuple[bool, int]:
        """Check pool liquidity with retry logic"""
        try:
            pool_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(pool_address),
                abi=self.pool_abi
            )
            
            liquidity = pool_contract.functions.liquidity().call()
            has_sufficient_liquidity = liquidity >= min_threshold
            
            logger.debug(f"Pool {pool_address}: liquidity={liquidity}, threshold={min_threshold}")
            return has_sufficient_liquidity, liquidity
            
        except Exception as e:
            logger.error(f"❌ Liquidity check failed for {pool_address}: {e}")
            return False, 0
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type((Web3Exception, ConnectionError))
    )
    def get_latest_block(self) -> int:
        """Get latest block number with retry logic"""
        try:
            return self.w3.eth.block_number
        except Exception as e:
            logger.error(f"❌ Failed to get latest block: {e}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type((Web3Exception, ConnectionError))
    )
    def create_event_filter(self, from_block: int, to_block: int):
        """Create event filter for PoolCreated events with retry logic"""
        try:
            return self.contract.events.PoolCreated.create_filter(
                from_block=from_block,
                to_block=to_block
            )
        except Exception as e:
            logger.error(f"❌ Failed to create event filter: {e}")
            raise
    
    @retry(
        stop=stop_after_attempt(5),  # More retries for event retrieval
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Web3Exception, ConnectionError))
    )
    def get_events(self, event_filter):
        """Get events from filter with retry logic - CRITICAL FIX"""
        try:
            events = event_filter.get_all_entries()
            logger.debug(f"✅ Retrieved {len(events)} events successfully")
            return events
        except Exception as e:
            logger.error(f"❌ Failed to get events (retrying...): {e}")
            raise  # Let retry decorator handle this 
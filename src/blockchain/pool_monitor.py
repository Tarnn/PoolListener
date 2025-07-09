"""
Pool Monitor
- Event processing and filtering
- Liquidity monitoring
- Notification triggering
"""

import asyncio
import time
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

class PoolMonitor:
    """Monitor Uniswap pools for target token"""
    
    def __init__(self, web3_client, db, notification_manager, settings, metrics_server=None):
        self.web3_client = web3_client
        self.db = db
        self.notification_manager = notification_manager
        self.settings = settings
        self.metrics_server = metrics_server
        self.executor = ThreadPoolExecutor(max_workers=settings.max_worker_threads)
        self.latest_processed_block = self.web3_client.get_latest_block()
        
    async def start_monitoring(self):
        """Start the main monitoring loop"""
        logger.info(f"🔍 Starting {self.settings.token_symbol} pool monitoring...")
        logger.info(f"📍 Target token: {self.settings.token_address}")
        logger.info(f"💰 Minimum liquidity: {self.settings.min_liquidity_threshold:,}")
        
        while True:
            try:
                await self._monitor_cycle()
                await asyncio.sleep(self.settings.polling_interval)
                
            except KeyboardInterrupt:
                logger.info("👋 Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"💥 Error in monitoring cycle: {e}")
                await asyncio.sleep(30)  # Wait before retrying
    
    async def _monitor_cycle(self):
        """Single monitoring cycle"""
        # Check for new pools
        await self._check_new_pools()
        
        # Check existing pools for liquidity changes
        await self._check_existing_pools()
        
        # Update active pools metric
        if self.metrics_server:
            stats = self.db.get_stats()
            self.metrics_server.active_pools_gauge.set(stats.get('total_pools', 0))
    
    async def _check_new_pools(self):
        """Check for new pool creation events"""
        try:
            current_block = self.web3_client.get_latest_block()
            
            if current_block <= self.latest_processed_block:
                return
            
            # Calculate block range
            from_block = self.latest_processed_block + 1
            blocks_to_check = current_block - from_block + 1
            
            logger.debug(f"🔍 Checking blocks {from_block} to {current_block} ({blocks_to_check} blocks)")
            
            # If too many blocks, process in chunks to avoid RPC limits
            MAX_BLOCKS_PER_QUERY = 1000  # Safe limit for most RPC providers
            
            if blocks_to_check > MAX_BLOCKS_PER_QUERY:
                logger.info(f"📦 Large block range detected ({blocks_to_check} blocks), processing in chunks...")
                
                # Process in chunks
                for chunk_start in range(from_block, current_block + 1, MAX_BLOCKS_PER_QUERY):
                    chunk_end = min(chunk_start + MAX_BLOCKS_PER_QUERY - 1, current_block)
                    
                    logger.debug(f"📦 Processing chunk: {chunk_start} to {chunk_end}")
                    
                    # Create event filter for chunk
                    event_filter = self.web3_client.create_event_filter(
                        from_block=chunk_start,
                        to_block=chunk_end
                    )
                    
                    if event_filter:
                        # Get events for this chunk
                        events = self.web3_client.get_events(event_filter)
                        
                        for event in events:
                            await self._process_pool_event(event)
                    
                    # Update progress
                    self.latest_processed_block = chunk_end
                    
                    # Small delay between chunks to be nice to RPC
                    await asyncio.sleep(0.1)
            else:
                # Normal processing for small ranges
                event_filter = self.web3_client.create_event_filter(
                    from_block=from_block,
                    to_block=current_block
                )
                
                if event_filter:
                    events = self.web3_client.get_events(event_filter)
                    
                    for event in events:
                        await self._process_pool_event(event)
                
                self.latest_processed_block = current_block
            
        except Exception as e:
            logger.error(f"❌ Error checking new pools: {e}")
    
    async def _process_pool_event(self, event):
        """Process a pool creation event"""
        try:
            token0 = event['args']['token0'].lower()
            token1 = event['args']['token1'].lower()
            fee = event['args']['fee']
            pool_address = event['args']['pool'].lower()
            
            # Check if involves target token
            if not self._involves_target_token(token0, token1):
                return
            
            logger.info(f"🎉 NEW {self.settings.token_symbol} POOL DISCOVERED!")
            logger.info(f"📍 Pool: {pool_address}")
            logger.info(f"💸 Fee: {fee} basis points")
            
            # Update metrics
            if self.metrics_server:
                self.metrics_server.pools_discovered_total.labels(
                    token_symbol=self.settings.token_symbol
                ).inc()
            
            # Check initial liquidity
            has_liquidity, liquidity_amount = self.web3_client.check_pool_liquidity(
                pool_address, self.settings.min_liquidity_threshold
            )
            
            # Update liquidity check metrics
            if self.metrics_server:
                status = "sufficient" if has_liquidity else "insufficient"
                self.metrics_server.liquidity_checks_total.labels(status=status).inc()
            
            # Save to database
            pool_data = {
                'address': pool_address,
                'token0': token0,
                'token1': token1,
                'fee': fee,
                'liquidity': liquidity_amount
            }
            self.db.save_pool(pool_data)
            
            # Send notification
            notification_type = "liquidity_added" if has_liquidity else "pool_created"
            
            if has_liquidity:
                logger.info(f"💰 POOL HAS SUFFICIENT LIQUIDITY: {liquidity_amount:,} - TRADEABLE! 🚀")
            else:
                logger.info(f"⚠️  Pool has insufficient liquidity: {liquidity_amount:,}")
                logger.info("📡 Will monitor this pool for liquidity additions...")
            
            # Time the notification sending
            start_time = time.time()
            await self.notification_manager.send_notification(
                pool_address, token0, token1, fee, liquidity_amount, notification_type
            )
            
            # Update notification metrics
            if self.metrics_server:
                notification_time = time.time() - start_time
                self.metrics_server.notification_latency_seconds.observe(notification_time)
                self.metrics_server.notifications_sent_total.labels(
                    notification_type=notification_type,
                    channel="multi"
                ).inc()
            
        except Exception as e:
            logger.error(f"❌ Error processing pool event: {e}")
    
    async def _check_existing_pools(self):
        """Check existing pools for liquidity changes"""
        try:
            non_tradeable_pools = self.db.get_non_tradeable_pools()
            
            if not non_tradeable_pools:
                return
            
            logger.debug(f"🔍 Checking {len(non_tradeable_pools)} pools for liquidity changes")
            
            # Check pools in parallel
            loop = asyncio.get_event_loop()
            tasks = []
            
            for pool_data in non_tradeable_pools:
                task = loop.run_in_executor(
                    self.executor,
                    self._check_single_pool,
                    pool_data
                )
                tasks.append(task)
            
            # Wait for all checks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"❌ Pool check error: {result}")
                    
        except Exception as e:
            logger.error(f"❌ Error checking existing pools: {e}")
    
    def _check_single_pool(self, pool_data: Dict):
        """Check a single pool's liquidity (runs in thread pool)"""
        try:
            pool_address = pool_data['address']
            has_liquidity, current_liquidity = self.web3_client.check_pool_liquidity(
                pool_address, self.settings.min_liquidity_threshold
            )
            
            # Update liquidity check metrics
            if self.metrics_server:
                status = "sufficient" if has_liquidity else "insufficient"
                self.metrics_server.liquidity_checks_total.labels(status=status).inc()
            
            # If pool became tradeable
            if has_liquidity and not pool_data['is_tradeable']:
                logger.info(f"🚀 POOL BECAME TRADEABLE!")
                logger.info(f"📍 Pool: {pool_address}")
                logger.info(f"💰 Liquidity: {current_liquidity:,}")
                
                # Update database
                self.db.mark_pool_tradeable(pool_address, current_liquidity)
                
                # Send notification (schedule on main thread)
                async def send_notification():
                    start_time = time.time()
                    await self.notification_manager.send_notification(
                        pool_address,
                        pool_data['token0'],
                        pool_data['token1'],
                        pool_data['fee'],
                        current_liquidity,
                        "liquidity_added"
                    )
                    
                    # Update notification metrics
                    if self.metrics_server:
                        notification_time = time.time() - start_time
                        self.metrics_server.notification_latency_seconds.observe(notification_time)
                        self.metrics_server.notifications_sent_total.labels(
                            notification_type="liquidity_added",
                            channel="multi"
                        ).inc()
                
                asyncio.create_task(send_notification())
                
        except Exception as e:
            logger.error(f"❌ Error checking single pool: {e}")
    
    def _involves_target_token(self, token0: str, token1: str) -> bool:
        """Check if either token matches our target"""
        return (token0.lower() == self.settings.token_address.lower() or 
                token1.lower() == self.settings.token_address.lower()) 
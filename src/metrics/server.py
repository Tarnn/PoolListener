"""
Metrics Server
- Prometheus metrics collection
- Health monitoring dashboard
- Performance tracking
"""

import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading
import time
from datetime import datetime
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry

logger = logging.getLogger(__name__)

class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP handler for metrics and dashboard"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_dashboard()
        elif parsed_path.path == '/metrics':
            self.serve_metrics()
        elif parsed_path.path == '/health':
            self.serve_health()
        else:
            self.send_error(404, "Not Found")
    
    def serve_dashboard(self):
        """Serve HTML dashboard"""
        dashboard_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🔍 Pool Listener Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            text-align: center;
            margin-bottom: 40px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.15);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #4CAF50;
        }}
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .status {{
            background: rgba(76, 175, 80, 0.2);
            color: #4CAF50;
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin: 10px;
            border: 2px solid #4CAF50;
        }}
        .links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }}
        .link {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 25px;
            border: 2px solid white;
            transition: all 0.3s ease;
        }}
        .link:hover {{
            background: white;
            color: #667eea;
        }}
        .refresh {{
            text-align: center;
            margin-top: 20px;
            opacity: 0.7;
        }}
    </style>
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(function() {{
            location.reload();
        }}, 30000);
    </script>
</head>
<body>
    <div class="container">
        <h1>🔍 Enhanced Pool Listener Dashboard</h1>
        
        <div class="status">
            🚀 ACTIVE - Monitoring {self.server.metrics_server.get_token_symbol()} Pools
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{self.server.metrics_server.get_pools_discovered()}</div>
                <div class="stat-label">📊 Pools Discovered</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.server.metrics_server.get_notifications_sent()}</div>
                <div class="stat-label">📧 Notifications Sent</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.server.metrics_server.get_liquidity_checks()}</div>
                <div class="stat-label">💰 Liquidity Checks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{self.server.metrics_server.get_active_pools()}</div>
                <div class="stat-label">🎯 Active Pools</div>
            </div>
        </div>
        
        <div class="links">
            <a href="/metrics" class="link">📊 Prometheus Metrics</a>
            <a href="/health" class="link">❤️ Health Check</a>
        </div>
        
        <div class="refresh">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | Auto-refresh in 30s
        </div>
    </div>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(dashboard_html.encode('utf-8'))
    
    def serve_metrics(self):
        """Serve Prometheus metrics"""
        metrics_data = generate_latest(self.server.metrics_server.registry)
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; version=0.0.4; charset=utf-8')
        self.end_headers()
        self.wfile.write(metrics_data)
    
    def serve_health(self):
        """Serve health check"""
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": time.time() - self.server.metrics_server.start_time,
            "pools_discovered": self.server.metrics_server.get_pools_discovered(),
            "notifications_sent": self.server.metrics_server.get_notifications_sent()
        }
        
        import json
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(health_data, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass  # Suppress default HTTP server logs

class MetricsServer:
    """Enhanced metrics server with dashboard"""
    
    def __init__(self, port: int):
        self.port = port
        self.registry = CollectorRegistry()
        self.start_time = time.time()
        self.token_symbol = "Unknown"
        self.setup_metrics()
        self.server = None
    
    def setup_metrics(self):
        """Setup Prometheus metrics"""
        
        self.pools_discovered_total = Counter(
            'pools_discovered_total',
            'Total number of pools discovered',
            ['token_symbol'],
            registry=self.registry
        )
        
        self.notifications_sent_total = Counter(
            'notifications_sent_total',
            'Total notifications sent',
            ['notification_type', 'channel'],
            registry=self.registry
        )
        
        self.liquidity_checks_total = Counter(
            'liquidity_checks_total',
            'Total liquidity checks performed',
            ['status'],
            registry=self.registry
        )
        
        self.notification_latency_seconds = Histogram(
            'notification_latency_seconds',
            'Time taken to send notifications',
            registry=self.registry
        )
        
        self.active_pools_gauge = Gauge(
            'active_pools_total',
            'Number of pools being monitored',
            registry=self.registry
        )
    
    def set_token_symbol(self, symbol: str):
        """Set the token symbol for display"""
        self.token_symbol = symbol
    
    def get_token_symbol(self) -> str:
        """Get current token symbol"""
        return self.token_symbol
    
    def get_pools_discovered(self) -> int:
        """Get total pools discovered"""
        try:
            # Sum all values across different label combinations
            total = 0
            for sample in self.pools_discovered_total.collect()[0].samples:
                total += sample.value
            return int(total)
        except:
            return 0
    
    def get_notifications_sent(self) -> int:
        """Get total notifications sent"""
        try:
            # Sum all values across different label combinations
            total = 0
            for sample in self.notifications_sent_total.collect()[0].samples:
                total += sample.value
            return int(total)
        except:
            return 0
    
    def get_liquidity_checks(self) -> int:
        """Get total liquidity checks"""
        try:
            # Sum all values across different label combinations
            total = 0
            for sample in self.liquidity_checks_total.collect()[0].samples:
                total += sample.value
            return int(total)
        except:
            return 0
    
    def get_active_pools(self) -> int:
        """Get active pools count"""
        try:
            return int(self.active_pools_gauge._value.get())
        except:
            return 0
    
    def start(self):
        """Start metrics server"""
        try:
            self.server = HTTPServer(('0.0.0.0', self.port), MetricsHandler)
            self.server.metrics_server = self  # Pass reference
            
            # Start in background thread
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            logger.info(f"📊 Metrics server started on port {self.port}")
            logger.info(f"🔗 Dashboard: http://localhost:{self.port}/")
            logger.info(f"📈 Metrics: http://localhost:{self.port}/metrics")
            logger.info(f"❤️ Health: http://localhost:{self.port}/health")
            
        except Exception as e:
            logger.error(f"❌ Failed to start metrics server: {e}")
    
    def stop(self):
        """Stop metrics server"""
        if self.server:
            self.server.shutdown()
            logger.info("📊 Metrics server stopped") 
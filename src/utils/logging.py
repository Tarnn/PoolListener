"""
Logging Utilities
- Structured logging setup
- Colored console output
- Log level configuration
"""

import logging
import structlog
import colorama

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup structured logging with color output"""
    
    # Initialize colorama
    colorama.init()
    
    class ColoredFormatter(logging.Formatter):
        """Colored log formatter"""
        
        COLORS = {
            'DEBUG': colorama.Fore.CYAN,
            'INFO': colorama.Fore.GREEN,
            'WARNING': colorama.Fore.YELLOW,
            'ERROR': colorama.Fore.RED,
            'CRITICAL': colorama.Fore.MAGENTA
        }
        
        def format(self, record):
            log_color = self.COLORS.get(record.levelname, colorama.Fore.WHITE)
            record.levelname = f"{log_color}{record.levelname}{colorama.Style.RESET_ALL}"
            return super().format(record)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    # Apply colored formatter
    for handler in logging.root.handlers:
        handler.setFormatter(ColoredFormatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
    
    return logging.getLogger(__name__) 
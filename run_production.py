#!/usr/bin/env python
"""Production server runner with comprehensive crash protection."""
import os
import sys
import socket
import logging
import signal
from datetime import datetime

# Configure logging for production
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler('server.log', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

class ServerManager:
    def __init__(self):
        self.running = True
        self.crash_count = 0
        self.max_retries = 3
        
    def signal_handler(self, sig, frame):
        logger.info("Shutdown signal received")
        self.running = False
        sys.exit(0)
    
    def check_port(self, port=5000):
        """Check if port is available."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', port))
            s.close()
            logger.info(f"Port {port} is available")
            return True
        except OSError as e:
            logger.warning(f"Port {port} may be in use: {e}")
            return False
    
    def start_server(self):
        """Start the production server."""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info("=" * 60)
        logger.info("PC Builder Server - Production Mode")
        logger.info(f"Started at {datetime.now()}")
        logger.info("=" * 60)
        
        # Check port
        if not self.check_port(5000):
            logger.warning("Port 5000 may be in use, attempting to start anyway...")
        
        # Load Flask app
        try:
            from server.app import create_app
            app = create_app()
            logger.info("Flask app created successfully")
        except Exception as e:
            logger.critical(f"Failed to create Flask app: {e}", exc_info=True)
            sys.exit(1)
        
        # Start Waitress server
        try:
            from waitress import serve
            
            logger.info("Starting Waitress WSGI server...")
            logger.info("Server running at http://127.0.0.1:5000")
            logger.info("Press Ctrl+C to stop")
            logger.info("-" * 60)
            
            serve(
                app,
                host='127.0.0.1',
                port=5000,
                _quiet=False,
                threads=10,
                max_request_body_size=16777216,  # 16MB max request
                socket_options=[(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)],
                ident='PCBuilder/1.0',
                channel_timeout=120,
                log_socket_errors=True,
                cleanup_interval=30
            )
        except KeyboardInterrupt:
            logger.info("Server stopped by user (Ctrl+C)")
            sys.exit(0)
        except OSError as e:
            if "Address already in use" in str(e):
                logger.error(f"Port 5000 is already in use: {e}")
                sys.exit(1)
            else:
                logger.error(f"OS Error: {e}", exc_info=True)
                sys.exit(1)
        except Exception as e:
            logger.critical(f"Server error: {e}", exc_info=True)
            sys.exit(1)
        finally:
            logger.info("Server shutdown complete")

if __name__ == '__main__':
    manager = ServerManager()
    manager.start_server()

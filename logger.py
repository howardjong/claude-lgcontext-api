import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Configure logging with enhanced file and console handlers"""
    logger = logging.getLogger('claude_service')
    logger.setLevel(logging.DEBUG)

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # File handler with more detailed formatting
    file_handler = RotatingFileHandler(
        'logs/claude_service.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(pathname)s:%(lineno)d - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Console handler with color coding for different log levels
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)

    # Remove any existing handlers
    logger.handlers = []

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
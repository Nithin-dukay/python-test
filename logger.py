#!/usr/bin/env python3
"""
Logging Module
Provides structured logging with colored console output and file rotation.
"""

import logging
import logging.handlers
import os
from pathlib import Path
import colorlog


class LoggerManager:
    """Manages application logging with console and file handlers"""
    
    def __init__(self, name='app', log_dir='logs', log_level=logging.INFO):
        """
        Initialize the logger manager
        
        Args:
            name (str): Logger name
            log_dir (str): Directory for log files
            log_level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_level = log_level
        self.logger = None
        
    def setup_logger(self):
        """Set up logger with console and file handlers"""
        # Create logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.log_level)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s - %(message)s',
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        self._setup_file_handler()
        
        return self.logger
    
    def _setup_file_handler(self):
        """Set up rotating file handler"""
        # Create log directory if it doesn't exist
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = self.log_dir / f'{self.name}.log'
        
        # Rotating file handler (10MB max, keep 5 backups)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        """Get the configured logger instance"""
        if self.logger is None:
            self.setup_logger()
        return self.logger


def get_logger(name='app', log_dir='logs', log_level=logging.INFO):
    """
    Convenience function to get a configured logger
    
    Args:
        name (str): Logger name
        log_dir (str): Directory for log files
        log_level (int): Logging level
        
    Returns:
        logging.Logger: Configured logger instance
    """
    manager = LoggerManager(name=name, log_dir=log_dir, log_level=log_level)
    return manager.setup_logger()


def set_log_level(logger, level_name):
    """
    Set log level from string name
    
    Args:
        logger (logging.Logger): Logger instance
        level_name (str): Level name (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    level = level_map.get(level_name.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Update all handlers
    for handler in logger.handlers:
        handler.setLevel(level)

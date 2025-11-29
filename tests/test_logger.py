"""Tests for logger module"""

import pytest
import logging
from pathlib import Path

from logger import LoggerManager, get_logger, set_log_level


class TestLoggerManager:
    """Test cases for LoggerManager class"""
    
    def test_logger_initialization(self, temp_log_dir):
        """Test logger manager initialization"""
        manager = LoggerManager(name='test', log_dir=temp_log_dir, log_level=logging.INFO)
        
        assert manager.name == 'test'
        assert manager.log_dir == Path(temp_log_dir)
        assert manager.log_level == logging.INFO
    
    def test_setup_logger(self, temp_log_dir):
        """Test logger setup"""
        manager = LoggerManager(name='test', log_dir=temp_log_dir)
        logger = manager.setup_logger()
        
        assert logger is not None
        assert logger.name == 'test'
        assert len(logger.handlers) == 2  # Console and file handlers
    
    def test_get_logger(self, temp_log_dir):
        """Test getting logger instance"""
        manager = LoggerManager(name='test', log_dir=temp_log_dir)
        logger1 = manager.get_logger()
        logger2 = manager.get_logger()
        
        assert logger1 is logger2  # Should return same instance
    
    def test_log_file_creation(self, temp_log_dir):
        """Test that log file is created"""
        manager = LoggerManager(name='test', log_dir=temp_log_dir)
        logger = manager.setup_logger()
        
        logger.info("Test message")
        
        log_file = Path(temp_log_dir) / 'test.log'
        assert log_file.exists()
    
    def test_log_levels(self, temp_log_dir):
        """Test different log levels"""
        manager = LoggerManager(name='test', log_dir=temp_log_dir, log_level=logging.DEBUG)
        logger = manager.setup_logger()
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        log_file = Path(temp_log_dir) / 'test.log'
        content = log_file.read_text()
        
        assert "Debug message" in content
        assert "Info message" in content
        assert "Warning message" in content
        assert "Error message" in content
        assert "Critical message" in content
    
    def test_convenience_function(self, temp_log_dir):
        """Test get_logger convenience function"""
        logger = get_logger(name='test', log_dir=temp_log_dir, log_level=logging.INFO)
        
        assert logger is not None
        assert logger.name == 'test'
    
    def test_set_log_level_function(self, temp_log_dir):
        """Test set_log_level function"""
        logger = get_logger(name='test', log_dir=temp_log_dir, log_level=logging.INFO)
        
        set_log_level(logger, 'DEBUG')
        assert logger.level == logging.DEBUG
        
        set_log_level(logger, 'ERROR')
        assert logger.level == logging.ERROR
        
        set_log_level(logger, 'warning')  # Test case insensitivity
        assert logger.level == logging.WARNING
    
    def test_invalid_log_level(self, temp_log_dir):
        """Test handling of invalid log level"""
        logger = get_logger(name='test', log_dir=temp_log_dir, log_level=logging.INFO)
        
        # Should default to INFO for invalid level
        set_log_level(logger, 'INVALID')
        assert logger.level == logging.INFO
    
    def test_log_directory_creation(self):
        """Test that log directory is created if it doesn't exist"""
        import tempfile
        import shutil
        
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / 'nested' / 'logs'
            
            manager = LoggerManager(name='test', log_dir=str(log_dir))
            manager.setup_logger()
            
            assert log_dir.exists()
    
    def test_multiple_loggers(self, temp_log_dir):
        """Test creating multiple loggers"""
        logger1 = get_logger(name='app1', log_dir=temp_log_dir)
        logger2 = get_logger(name='app2', log_dir=temp_log_dir)
        
        logger1.info("Message from app1")
        logger2.info("Message from app2")
        
        log_file1 = Path(temp_log_dir) / 'app1.log'
        log_file2 = Path(temp_log_dir) / 'app2.log'
        
        assert log_file1.exists()
        assert log_file2.exists()
        
        assert "Message from app1" in log_file1.read_text()
        assert "Message from app2" in log_file2.read_text()

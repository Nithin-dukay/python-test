"""Tests for configuration manager module"""

import pytest
import tempfile
import os
from pathlib import Path

from config_manager import ConfigManager, ConfigurationError, load_config


class TestConfigManager:
    """Test cases for ConfigManager class"""
    
    def test_load_default_config(self):
        """Test loading default configuration when file doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / 'nonexistent.yaml'
            manager = ConfigManager(str(config_path))
            config = manager.load_config()
            
            assert 'app' in config
            assert 'logging' in config
            assert 'connectivity' in config
            assert 'selenium' in config
    
    def test_load_config_from_file(self, temp_config_file):
        """Test loading configuration from file"""
        manager = ConfigManager(temp_config_file)
        config = manager.load_config()
        
        assert config['app']['name'] == 'Test App'
        assert config['app']['port'] == 8080
        assert config['logging']['level'] == 'DEBUG'
    
    def test_save_config(self, sample_config):
        """Test saving configuration to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / 'test_config.yaml'
            manager = ConfigManager(str(config_path))
            
            manager.save_config(sample_config)
            
            assert config_path.exists()
            
            # Load and verify
            manager2 = ConfigManager(str(config_path))
            loaded_config = manager2.load_config()
            assert loaded_config['app']['name'] == 'Test App'
    
    def test_get_config_value(self, sample_config):
        """Test getting configuration values using dot notation"""
        manager = ConfigManager()
        manager.config = sample_config
        
        assert manager.get('app.name') == 'Test App'
        assert manager.get('app.port') == 8080
        assert manager.get('logging.level') == 'INFO'
        assert manager.get('nonexistent.key', 'default') == 'default'
    
    def test_set_config_value(self):
        """Test setting configuration values using dot notation"""
        manager = ConfigManager()
        manager.config = {}
        
        manager.set('app.name', 'New App')
        manager.set('app.port', 9000)
        
        assert manager.config['app']['name'] == 'New App'
        assert manager.config['app']['port'] == 9000
    
    def test_validate_valid_config(self, sample_config):
        """Test validation of valid configuration"""
        manager = ConfigManager()
        manager.config = sample_config
        
        assert manager.validate() is True
    
    def test_validate_invalid_port(self, sample_config):
        """Test validation fails for invalid port"""
        manager = ConfigManager()
        sample_config['app']['port'] = 99999
        manager.config = sample_config
        
        with pytest.raises(ConfigurationError, match="Invalid port number"):
            manager.validate()
    
    def test_validate_invalid_log_level(self, sample_config):
        """Test validation fails for invalid log level"""
        manager = ConfigManager()
        sample_config['logging']['level'] = 'INVALID'
        manager.config = sample_config
        
        with pytest.raises(ConfigurationError, match="Invalid log level"):
            manager.validate()
    
    def test_validate_invalid_timeout(self, sample_config):
        """Test validation fails for invalid timeout"""
        manager = ConfigManager()
        sample_config['connectivity']['timeout'] = -1
        manager.config = sample_config
        
        with pytest.raises(ConfigurationError, match="Invalid timeout value"):
            manager.validate()
    
    def test_env_override(self, sample_config, monkeypatch):
        """Test environment variable overrides"""
        monkeypatch.setenv('APP_PORT', '7000')
        monkeypatch.setenv('LOG_LEVEL', 'DEBUG')
        
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / 'test.yaml'
            manager = ConfigManager(str(config_path))
            manager.save_config(sample_config)
            
            config = manager.load_config()
            
            assert config['app']['port'] == 7000
            assert config['logging']['level'] == 'DEBUG'
    
    def test_get_all_config(self, sample_config):
        """Test getting entire configuration"""
        manager = ConfigManager()
        manager.config = sample_config
        
        all_config = manager.get_all()
        
        assert all_config == sample_config
        assert all_config is not sample_config  # Should be a copy
    
    def test_load_config_convenience_function(self, temp_config_file):
        """Test convenience function for loading config"""
        config = load_config(temp_config_file)
        
        assert config['app']['name'] == 'Test App'
        assert 'logging' in config
    
    def test_invalid_yaml_file(self):
        """Test handling of invalid YAML file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_path = f.name
        
        try:
            manager = ConfigManager(temp_path)
            with pytest.raises(ConfigurationError, match="Invalid YAML"):
                manager.load_config()
        finally:
            os.unlink(temp_path)
    
    def test_merge_with_defaults(self):
        """Test merging user config with defaults"""
        manager = ConfigManager()
        user_config = {
            'app': {
                'port': 9000
            }
        }
        
        merged = manager._merge_with_defaults(user_config)
        
        # Should have default values
        assert 'name' in merged['app']
        assert 'logging' in merged
        # Should have user override
        assert merged['app']['port'] == 9000

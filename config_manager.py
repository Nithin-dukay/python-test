#!/usr/bin/env python3
"""
Configuration Manager Module
Handles loading, saving, and validating YAML configuration files.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass


class ConfigManager:
    """Manages application configuration from YAML files and environment variables"""
    
    DEFAULT_CONFIG = {
        'app': {
            'name': 'Python Test App',
            'version': '1.0.0',
            'host': '0.0.0.0',
            'port': 5000,
            'debug': True
        },
        'logging': {
            'level': 'INFO',
            'directory': 'logs',
            'max_file_size_mb': 10,
            'backup_count': 5
        },
        'connectivity': {
            'timeout': 10,
            'targets': ['https://www.google.com', 'https://www.bing.com']
        },
        'selenium': {
            'headless': False,
            'window_size': '1920x1080',
            'timeout': 10
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_path (str, optional): Path to configuration file
        """
        self.config_path = Path(config_path) if config_path else Path('config.yaml')
        self.config = {}
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults
        
        Returns:
            dict: Configuration dictionary
            
        Raises:
            ConfigurationError: If config file is invalid
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise ConfigurationError(f"Invalid YAML in config file: {e}")
            except Exception as e:
                raise ConfigurationError(f"Error reading config file: {e}")
        else:
            self.config = self.DEFAULT_CONFIG.copy()
        
        # Merge with defaults to ensure all keys exist
        self.config = self._merge_with_defaults(self.config)
        
        # Override with environment variables
        self._apply_env_overrides()
        
        return self.config
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Save configuration to file
        
        Args:
            config (dict, optional): Configuration to save. Uses current config if None.
            
        Raises:
            ConfigurationError: If unable to save config
        """
        if config is not None:
            self.config = config
        
        try:
            # Create directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        except Exception as e:
            raise ConfigurationError(f"Error saving config file: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path (str): Dot-separated path to config value (e.g., 'app.port')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation
        
        Args:
            key_path (str): Dot-separated path to config value
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def validate(self) -> bool:
        """
        Validate configuration values
        
        Returns:
            bool: True if valid
            
        Raises:
            ConfigurationError: If validation fails
        """
        # Validate port number
        port = self.get('app.port')
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ConfigurationError(f"Invalid port number: {port}")
        
        # Validate log level
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        log_level = self.get('logging.level', '').upper()
        if log_level not in valid_levels:
            raise ConfigurationError(f"Invalid log level: {log_level}")
        
        # Validate timeout
        timeout = self.get('connectivity.timeout')
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ConfigurationError(f"Invalid timeout value: {timeout}")
        
        return True
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge configuration with defaults
        
        Args:
            config (dict): User configuration
            
        Returns:
            dict: Merged configuration
        """
        merged = self.DEFAULT_CONFIG.copy()
        
        for section, values in config.items():
            if section in merged and isinstance(values, dict):
                merged[section].update(values)
            else:
                merged[section] = values
        
        return merged
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides"""
        # APP_PORT -> app.port
        env_mappings = {
            'APP_PORT': 'app.port',
            'APP_HOST': 'app.host',
            'APP_DEBUG': 'app.debug',
            'LOG_LEVEL': 'logging.level',
            'LOG_DIR': 'logging.directory',
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert boolean strings
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                # Convert numeric strings
                elif value.isdigit():
                    value = int(value)
                
                self.set(config_key, value)
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get entire configuration
        
        Returns:
            dict: Complete configuration dictionary
        """
        return self.config.copy()


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to load configuration
    
    Args:
        config_path (str, optional): Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    manager = ConfigManager(config_path)
    return manager.load_config()

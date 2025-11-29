"""Pytest configuration and fixtures"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
app:
  name: Test App
  version: 1.0.0
  host: localhost
  port: 8080
  debug: false

logging:
  level: DEBUG
  directory: test_logs
  max_file_size_mb: 5
  backup_count: 3

connectivity:
  timeout: 5
  targets:
    - https://example.com

selenium:
  headless: true
  window_size: 1024x768
  timeout: 5
""")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_log_dir():
    """Create a temporary log directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_config():
    """Provide a sample configuration dictionary"""
    return {
        'app': {
            'name': 'Test App',
            'version': '1.0.0',
            'host': 'localhost',
            'port': 8080,
            'debug': False
        },
        'logging': {
            'level': 'INFO',
            'directory': 'logs',
            'max_file_size_mb': 10,
            'backup_count': 5
        },
        'connectivity': {
            'timeout': 10,
            'targets': ['https://www.google.com']
        },
        'selenium': {
            'headless': True,
            'window_size': '1920x1080',
            'timeout': 10
        }
    }

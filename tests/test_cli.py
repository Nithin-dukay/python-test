"""Tests for CLI module"""

import pytest
from click.testing import CliRunner
import tempfile
from pathlib import Path

from cli import cli, version


class TestCLI:
    """Test cases for CLI commands"""
    
    def test_cli_help(self):
        """Test CLI help command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'Python Test App' in result.output
        assert 'run-app' in result.output
        assert 'check-connectivity' in result.output
        assert 'test-selenium' in result.output
    
    def test_version_command(self, temp_config_file):
        """Test version command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'version'])
        
        assert result.exit_code == 0
        assert 'Test App' in result.output
        assert '1.0.0' in result.output
    
    def test_config_show_command(self, temp_config_file):
        """Test config show command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'config', 'show'])
        
        assert result.exit_code == 0
        assert 'app:' in result.output
        assert 'logging:' in result.output
    
    def test_config_get_command(self, temp_config_file):
        """Test config get command"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'config', 'get', 'app.port'])
        
        assert result.exit_code == 0
        assert '8080' in result.output
    
    def test_config_get_nonexistent_key(self, temp_config_file):
        """Test config get with nonexistent key"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'config', 'get', 'nonexistent.key'])
        
        assert result.exit_code == 1
        assert 'not found' in result.output
    
    def test_config_set_command(self):
        """Test config set command"""
        runner = CliRunner()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("app:\n  name: Test\n  port: 5000\n")
            temp_path = f.name
        
        try:
            result = runner.invoke(cli, ['--config', temp_path, 'config', 'set', 'app.port', '9000'])
            
            assert result.exit_code == 0
            assert 'Set app.port = 9000' in result.output
            
            # Verify the change
            result2 = runner.invoke(cli, ['--config', temp_path, 'config', 'get', 'app.port'])
            assert '9000' in result2.output
        finally:
            import os
            os.unlink(temp_path)
    
    def test_verbose_flag(self, temp_config_file):
        """Test verbose flag"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, '--verbose', 'version'])
        
        assert result.exit_code == 0
    
    def test_log_level_option(self, temp_config_file):
        """Test log level option"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, '--log-level', 'DEBUG', 'version'])
        
        assert result.exit_code == 0
    
    def test_invalid_config_file(self):
        """Test handling of invalid config file"""
        runner = CliRunner()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: [")
            temp_path = f.name
        
        try:
            result = runner.invoke(cli, ['--config', temp_path, 'version'])
            assert result.exit_code == 1
            assert 'Configuration error' in result.output
        finally:
            import os
            os.unlink(temp_path)
    
    def test_check_connectivity_help(self, temp_config_file):
        """Test check-connectivity help"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'check-connectivity', '--help'])
        
        assert result.exit_code == 0
        assert 'Check connectivity' in result.output
        assert '--target' in result.output
        assert '--timeout' in result.output
    
    def test_test_selenium_help(self, temp_config_file):
        """Test test-selenium help"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'test-selenium', '--help'])
        
        assert result.exit_code == 0
        assert 'Selenium' in result.output
        assert '--url' in result.output
        assert '--headless' in result.output
    
    def test_run_app_help(self, temp_config_file):
        """Test run-app help"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'run-app', '--help'])
        
        assert result.exit_code == 0
        assert 'Flask' in result.output
        assert '--host' in result.output
        assert '--port' in result.output
    
    def test_config_command_group(self, temp_config_file):
        """Test config command group"""
        runner = CliRunner()
        result = runner.invoke(cli, ['--config', temp_config_file, 'config', '--help'])
        
        assert result.exit_code == 0
        assert 'show' in result.output
        assert 'get' in result.output
        assert 'set' in result.output

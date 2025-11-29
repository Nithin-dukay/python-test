#!/usr/bin/env python3
"""
CLI Interface for Python Test App
Provides a unified command-line interface for all application features.
"""

import click
import sys
import logging
from pathlib import Path

from config_manager import ConfigManager, ConfigurationError
from logger import get_logger, set_log_level


# Global configuration and logger
config_manager = None
logger = None


def initialize_app(config_path, verbose, log_level):
    """Initialize application configuration and logging"""
    global config_manager, logger
    
    # Load configuration
    try:
        config_manager = ConfigManager(config_path)
        config = config_manager.load_config()
        config_manager.validate()
    except ConfigurationError as e:
        click.echo(f"Configuration error: {e}", err=True)
        sys.exit(1)
    
    # Determine log level
    if verbose:
        level = logging.DEBUG
    elif log_level:
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        level = level_map.get(log_level.upper(), logging.INFO)
    else:
        level_name = config_manager.get('logging.level', 'INFO')
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        level = level_map.get(level_name.upper(), logging.INFO)
    
    # Setup logger
    log_dir = config_manager.get('logging.directory', 'logs')
    logger = get_logger(name='cli', log_dir=log_dir, log_level=level)
    
    return config, logger


@click.group()
@click.option('--config', '-c', default='config.yaml', help='Path to configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output (DEBUG level)')
@click.option('--log-level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False), help='Set log level')
@click.pass_context
def cli(ctx, config, verbose, log_level):
    """Python Test App - Unified CLI for all features"""
    ctx.ensure_object(dict)
    
    # Initialize app
    app_config, app_logger = initialize_app(config, verbose, log_level)
    
    # Store in context
    ctx.obj['config'] = app_config
    ctx.obj['logger'] = app_logger
    ctx.obj['config_manager'] = config_manager


@cli.command()
@click.option('--host', '-h', help='Host to bind to')
@click.option('--port', '-p', type=int, help='Port to bind to')
@click.option('--debug/--no-debug', default=None, help='Enable debug mode')
@click.pass_context
def run_app(ctx, host, port, debug):
    """Start the Flask web application"""
    logger = ctx.obj['logger']
    config = ctx.obj['config']
    
    logger.info("Starting Flask application...")
    
    # Override config with CLI options
    app_host = host or config['app']['host']
    app_port = port or config['app']['port']
    app_debug = debug if debug is not None else config['app']['debug']
    
    logger.info(f"Host: {app_host}, Port: {app_port}, Debug: {app_debug}")
    
    try:
        # Import and run Flask app
        from app import app
        app.run(host=app_host, port=app_port, debug=app_debug)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        sys.exit(1)


@cli.command()
@click.option('--target', '-t', multiple=True, help='Target URL to check (can be specified multiple times)')
@click.option('--timeout', type=int, help='Request timeout in seconds')
@click.option('--simple', is_flag=True, help='Use simple check (HTTP only)')
@click.pass_context
def check_connectivity(ctx, target, timeout, simple):
    """Check connectivity to websites (Google, Bing, or custom targets)"""
    logger = ctx.obj['logger']
    config = ctx.obj['config']
    
    # Get targets
    targets = list(target) if target else config['connectivity']['targets']
    check_timeout = timeout or config['connectivity']['timeout']
    
    logger.info(f"Checking connectivity to {len(targets)} target(s)...")
    
    if simple:
        # Simple HTTP check
        import requests
        for url in targets:
            try:
                logger.info(f"Checking {url}...")
                response = requests.get(url, timeout=check_timeout)
                if response.status_code == 200:
                    click.echo(f"✅ {url} is UP (Status: {response.status_code})")
                    logger.info(f"{url} is accessible")
                else:
                    click.echo(f"⚠️  {url} returned status {response.status_code}")
                    logger.warning(f"{url} returned status {response.status_code}")
            except Exception as e:
                click.echo(f"❌ {url} is DOWN: {e}")
                logger.error(f"{url} is not accessible: {e}")
    else:
        # Comprehensive check
        for url in targets:
            if 'google.com' in url.lower():
                logger.info("Running comprehensive Google connectivity check...")
                from check_google import GoogleConnectivityChecker
                checker = GoogleConnectivityChecker()
                checker.timeout = check_timeout
                checker.run_comprehensive_check()
            elif 'bing.com' in url.lower():
                logger.info("Running comprehensive Bing connectivity check...")
                from check_bing import BingConnectivityChecker
                checker = BingConnectivityChecker()
                checker.timeout = check_timeout
                checker.run_comprehensive_check()
            else:
                # Generic check
                import requests
                try:
                    logger.info(f"Checking {url}...")
                    response = requests.get(url, timeout=check_timeout)
                    click.echo(f"✅ {url} is UP (Status: {response.status_code})")
                    logger.info(f"{url} is accessible")
                except Exception as e:
                    click.echo(f"❌ {url} is DOWN: {e}")
                    logger.error(f"{url} is not accessible: {e}")


@cli.command()
@click.option('--url', '-u', default='https://www.google.com', help='URL to navigate to')
@click.option('--headless/--no-headless', default=None, help='Run browser in headless mode')
@click.option('--timeout', type=int, help='Page load timeout in seconds')
@click.pass_context
def test_selenium(ctx, url, headless, timeout):
    """Run Selenium browser automation test"""
    logger = ctx.obj['logger']
    config = ctx.obj['config']
    
    logger.info("Starting Selenium browser test...")
    
    # Get configuration
    use_headless = headless if headless is not None else config['selenium']['headless']
    test_timeout = timeout or config['selenium']['timeout']
    
    logger.info(f"URL: {url}, Headless: {use_headless}, Timeout: {test_timeout}")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        if use_headless:
            chrome_options.add_argument("--headless")
        
        logger.info("Setting up Chrome driver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            logger.info(f"Navigating to {url}...")
            driver.get(url)
            
            WebDriverWait(driver, test_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            click.echo(f"✅ Successfully loaded: {driver.title}")
            click.echo(f"   Current URL: {driver.current_url}")
            logger.info(f"Page loaded successfully: {driver.title}")
            
        finally:
            logger.info("Closing browser...")
            driver.quit()
            
    except Exception as e:
        click.echo(f"❌ Selenium test failed: {e}")
        logger.error(f"Selenium test failed: {e}")
        sys.exit(1)


@cli.group(name='config')
@click.pass_context
def config_cmd(ctx):
    """Manage application configuration"""
    pass


@config_cmd.command('show')
@click.pass_context
def config_show(ctx):
    """Show current configuration"""
    config = ctx.obj['config']
    
    import yaml
    click.echo(yaml.dump(config, default_flow_style=False, sort_keys=False))


@config_cmd.command('get')
@click.argument('key')
@click.pass_context
def config_get(ctx, key):
    """Get a configuration value (use dot notation, e.g., app.port)"""
    config_mgr = ctx.obj['config_manager']
    value = config_mgr.get(key)
    
    if value is not None:
        click.echo(f"{key}: {value}")
    else:
        click.echo(f"Key '{key}' not found", err=True)
        sys.exit(1)


@config_cmd.command('set')
@click.argument('key')
@click.argument('value')
@click.pass_context
def config_set(ctx, key, value):
    """Set a configuration value (use dot notation, e.g., app.port 8080)"""
    config_mgr = ctx.obj['config_manager']
    logger = ctx.obj['logger']
    
    # Try to convert value to appropriate type
    if value.lower() in ('true', 'false'):
        value = value.lower() == 'true'
    elif value.isdigit():
        value = int(value)
    elif value.replace('.', '', 1).isdigit():
        value = float(value)
    
    config_mgr.set(key, value)
    
    try:
        config_mgr.save_config()
        click.echo(f"✅ Set {key} = {value}")
        logger.info(f"Configuration updated: {key} = {value}")
    except ConfigurationError as e:
        click.echo(f"❌ Failed to save configuration: {e}", err=True)
        logger.error(f"Failed to save configuration: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Show application version"""
    config = ctx.obj['config']
    app_name = config['app']['name']
    app_version = config['app']['version']
    
    click.echo(f"{app_name} v{app_version}")


if __name__ == '__main__':
    cli(obj={})

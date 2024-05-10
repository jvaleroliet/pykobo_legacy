import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    """
    Load the configuration from the config.json file.
    If the file doesn't exist, create it with default values.
    """
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    if not os.path.exists(config_path):
        # Default configuration
        config = {"token": "default_token", "server_url": "https://kf.kobotoolbox.org/"}
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    return config

def save_config(config):
    """
    Save the configuration to the config.json file.
    """
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def get_token():
    """
    Get the token from the configuration.
    """
    config = load_config()
    return config['token']

def set_token(token):
    """
    Set the token in the configuration.
    """
    config = load_config()
    config['token'] = token
    save_config(config)

def get_server_url():
    """
    Get the server URL from the configuration.
    """
    config = load_config()
    return config['server_url']

def set_server_url(server_url):
    """
    Set the server URL in the configuration.
    """
    config = load_config()
    config['server_url'] = server_url
    save_config(config)

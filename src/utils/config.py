import os
import toml

def read_config(config_path="config.toml"):
    """
    Reads configuration variables from the config.toml file.
    Returns a dictionary of configuration values.
    """
    
    # Example usage:
    # config = read_config()
    # use_prompts = config.get("use_prompts", True)    
    
    config_file = os.path.join(os.getcwd(), config_path)
    if not os.path.isfile(config_file):
        print(f"Config file '{config_file}' not found.")
        return {}
    try:
        with open(config_file, "r") as f:
            config = toml.load(f)
        return config
    except Exception as e:
        print(f"Error reading config file: {e}")
        return {}

def get_config_value(key, default=None, config_path="config.toml"):
    """
    Returns the value of a specific configuration key from config.toml.
    If the key is not found, returns the provided default value.
    """
    config = read_config(config_path)
    return config.get(key, default)

import json

config_path = 'config.json'


def load_config():
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_config(config_data):
    with open(config_path, 'w') as file:
        json.dump(config_data, file, indent=4)


def get_api_key():
    """
    Return the value of the current API key stored in the config file.
    """
    try:
        config = load_config()

        if "API_KEY" not in config:
            raise KeyError("API_KEY is missing in the configuration file.")

        # Return the API key
        return config["API_KEY"]
    except FileNotFoundError:
        print("Error: Configuration file not found.")
        return None
    except KeyError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def set_api_key(api_key):
    """Update the API key in the configuration file."""
    config = load_config()
    config["API_KEY"] = api_key
    save_config(config)
    print(f"API key has been updated to: {api_key}")

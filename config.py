import os
from dotenv import load_dotenv
import requests
import json


load_dotenv()

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize_config()
        return cls._instance
    
    def _initialize_config(self):
        """
        Load and validate all necessary environment variables.

        The YOUTUBE_CHANNELS_CONFIG_JSON structure is expected to be:
        [
            {
                "name": str,
                "channel_url": str,
                "notion_database_id": str // the value stored actually is the env var key for the notion database id for that youtube channel
            },
            ...
        ]
        """
        self.ENVIRONMENT = self._get_env_var("ENVIRONMENT")
        self.NOTION_INTERNAL_INTEGRATION_SECRET = self._get_env_var("NOTION_INTERNAL_INTEGRATION_SECRET")
        self.NOTION_API_BASE_URL = self._get_env_var("NOTION_API_BASE_URL")

        if self.ENVIRONMENT == "local":
            with open('./youtube_channels_config.json', 'r') as file:
                self.YOUTUBE_CHANNELS_CONFIG_JSON = json.load(file)
                for youtube_channel in self.YOUTUBE_CHANNELS_CONFIG_JSON:
                    env_var_key_for_notion_database_id = youtube_channel["notion_database_id"]
                    notion_database_id_value = self._get_env_var(env_var_key_for_notion_database_id)
                    youtube_channel["notion_database_id"] = notion_database_id_value
        else:
            self.REMOTE_URL_FOR_YOUTUBE_CHANNELS_CONFIG_JSON = self._get_env_var("REMOTE_URL_FOR_YOUTUBE_CHANNELS_CONFIG_JSON")
            response = requests.get(self.REMOTE_URL_FOR_YOUTUBE_CHANNELS_CONFIG_JSON)
            if response.status_code == 200:
                self.YOUTUBE_CHANNELS_CONFIG_JSON = response.json()
                for youtube_channel in self.YOUTUBE_CHANNELS_CONFIG_JSON:
                    env_var_key_for_notion_database_id = youtube_channel["notion_database_id"]
                    notion_database_id_value = self._get_env_var(env_var_key_for_notion_database_id)
                    youtube_channel["notion_database_id"] = notion_database_id_value
            else:
                raise ConfigError(
                    f"Failed to fetch youtube channels config json from "
                    f"{self.REMOTE_URL_FOR_YOUTUBE_CHANNELS_CONFIG_JSON} \n"
                    f"Got status code: {response.status_code}"
                )


    def _get_env_var(self, key):
        """Retrieve an environment variable or raise an error if it's not set."""
        value = os.getenv(key)
        if value is None:
            raise ConfigError(f"Missing environment variable: {key}")
        return value

def get_config():
    return Config()
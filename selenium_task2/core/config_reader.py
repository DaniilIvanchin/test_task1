import json
import os

class ConfigReader:
    _config = None
    CONFIG_PATH = "config.json"

    @classmethod
    def load_config(cls):
        if cls._config is None:
            full_path = os.path.abspath(cls.CONFIG_PATH)
            with open(full_path, "r", encoding="utf-8") as f:
                cls._config = json.load(f)
        return cls._config

    @classmethod
    def get(cls, key, default=None):
        config = cls.load_config()
        return config.get(key, default)
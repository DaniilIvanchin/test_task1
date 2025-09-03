import json
import os

class ConfigReader:
    _config = None

    @classmethod
    def load_config(cls, path="config.json"):
        if cls._config is None:
            full_path = os.path.abspath(path)
            with open(full_path, "r", encoding="utf-8") as f:
                cls._config = json.load(f)
        return cls._config

    @classmethod
    def get(cls, key, default=None):
        config = cls.load_config()
        return config.get(key, default)
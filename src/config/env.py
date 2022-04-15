
from decouple import config as decouple_config

class Env:

    def __init__(self):
        self._config = {}

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def get_item(self, key: str, default=None):
        default_config = self._config[key] if key in self._config else default
        return decouple_config(key, default=default_config)


environment: Env = Env()
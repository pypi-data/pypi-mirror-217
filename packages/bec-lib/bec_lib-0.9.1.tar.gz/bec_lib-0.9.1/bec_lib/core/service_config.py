import json

import yaml

from .logger import bec_logger

logger = bec_logger.logger


class ServiceConfig:
    def __init__(
        self,
        config_path: str = None,
        scibec: dict = None,
        redis: dict = None,
        mongodb: dict = None,
        config: dict = None,
    ) -> None:
        self.config_path = config_path
        self.config = {}
        self._load_config()
        if self.config:
            self._load_urls("scibec", required=False)
            self._load_urls("redis", required=True)
            self._load_urls("mongodb", required=False)

        self._update_config(service_config=config, scibec=scibec, redis=redis, mongodb=mongodb)

        self.service_config = self.config.get("service_config", {})

    def _update_config(self, **kwargs):
        for key, val in kwargs.items():
            if not val:
                continue
            self.config[key] = val

    def _load_config(self):
        if not self.config_path:
            return
        with open(self.config_path, "r") as stream:
            self.config = yaml.safe_load(stream)
            logger.info(
                f"Loaded new config from disk: {json.dumps(self.config, sort_keys=True, indent=4)}"
            )

    def _load_urls(self, entry: str, required: bool = True):
        config = self.config.get(entry)
        if config:
            return f"{config['host']}:{config['port']}"

        if required:
            raise ValueError(
                f"The provided config does not specify the url (host and port) for {entry}."
            )
        return ""

    @property
    def scibec(self):
        return self._load_urls("scibec", required=False)

    @property
    def redis(self):
        return self._load_urls("redis", required=True)

    @property
    def mongodb(self):
        return self._load_urls("mongodb", required=False)

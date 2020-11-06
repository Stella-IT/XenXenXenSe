import os
from typing import Dict

import ujson


class Settings:
    @classmethod
    def is_docker(cls) -> bool:
        return "DOCKER_XXXS_CONFIG" in os.environ

    @classmethod
    def get_docker_config(cls) -> dict:
        load_config = ujson.loads(os.environ["DOCKER_XXXS_CONFIG"])
        return load_config

    @classmethod
    def get_xen_clusters(cls) -> Dict:
        """set xen credentials"""
        xen_clusters = {}
        if os.path.isfile("config.json"):
            with open("config.json", "r") as config_file:
                xen_clusters = ujson.load(config_file)["xen_clusters"]
            config_file.close()

        # Docker check
        if cls.is_docker():
            if "xen_clusters" in cls.get_docker_config():
                xen_clusters = cls.get_docker_config()["xen_clusters"]

        return xen_clusters

    @classmethod
    def get_mysql_credentials(cls) -> Dict:

        mysql_credentials = {}

        if os.path.isfile("config.json"):
            with open("config.json", "r") as config_file:
                mysql_credentials = ujson.load(config_file)[
                    "mysql_credentials"
                ]
            config_file.close()

        # Docker check
        if cls.is_docker():
            if "mysql_credentials" in cls.get_docker_config():
                mysql_credentials = cls.get_docker_config()[
                    "mysql_credentials"
                ]
        return mysql_credentials

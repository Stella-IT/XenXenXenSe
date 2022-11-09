import os
from typing import Dict, Union

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
    def get_config_json(cls) -> dict:
        if cls.is_docker():
            return cls.get_docker_config()
        else:
            if os.path.isfile("config.json"):
                result = None
                with open("config.json", "r") as config_file:
                    result = ujson.load(config_file)
                config_file.close()
                return result

    @classmethod
    def get_xen_clusters(cls) -> Dict:
        """get xen credentials"""
        xen_clusters = cls.get_config_json()["xen_clusters"]
        return xen_clusters

    @classmethod
    def get_authentication_config(cls) -> Union[Dict, None]:
        """get xen credentials"""
        authentication = cls.get_config_json()["authentication"]
        return authentication

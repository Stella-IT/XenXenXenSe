import os
from typing import Dict, Union

import ujson
import time


class Settings:
    config_filename = "config.json"

    config_cache = None
    config_last_modified = 0
    config_last_fetched = 0
    config_last_modified_fetched_at = 0
    config_last_modified_fetched_at_age = 10

    @classmethod
    def is_docker(cls) -> bool:
        return "DOCKER_XXXS_CONFIG" in os.environ

    @classmethod
    def get_docker_config(cls) -> dict:
        load_config = ujson.loads(os.environ["DOCKER_XXXS_CONFIG"])
        return load_config

    @classmethod
    def _fetch_config_from_file(cls) -> dict:
        try:
            if os.path.isfile(cls.config_filename):
                result = None
                with open(cls.config_filename, "r") as config_file:
                    result = ujson.load(config_file)
                config_file.close()

                cls.config_cache = result
                cls.config_last_fetched = time.time()
                return result
        except Exception as e:
            print("Failed")

    @classmethod
    def _is_config_modified(cls) -> bool:
        if cls.config_cache is None:
            return True

        if cls._is_config_last_modified_cache_expired():
            cls._fetch_last_modified_cache()

        return cls.config_last_fetched < cls.config_last_modified

    @classmethod
    def _fetch_last_modified_cache(cls) -> bool:
        cls.config_last_modified_fetched_at = time.time()
        cls.config_last_modified = os.path.getmtime(cls.config_filename)
        return cls.config_last_modified

    @classmethod
    def _is_config_last_modified_cache_expired(cls) -> bool:
        return cls.config_last_modified_fetched_at < time.time() - cls.config_last_modified_fetched_at_age

    @classmethod
    def get_config_json(cls) -> dict:
        if cls.is_docker():
            return cls.get_docker_config()
        else:
            if not cls._is_config_modified():
                return cls.config_cache

            if os.path.isfile(cls.config_filename):
                return cls._fetch_config_from_file()
            else:
                print("Error: XenXenXenSe has failed to initialize!")
                print()
                print("both config.json file and docker config environment variable (DOCKER_XXXS_CONFIG) are missing!")
                print("Please configure XenXenXenSe!")
                exit(1)

    @classmethod
    def get_xen_clusters(cls) -> Dict:
        """get xen credentials"""
        xen_clusters = cls.get_config_json()["xen_clusters"]
        return xen_clusters

    @classmethod
    def get_authentication_config(cls) -> Union[Dict, None]:
        """get authentication settings"""
        config = cls.get_config_json()
        if "authentication" in config:
            return config["authentication"]

        return None

class MissingConfigFile(IOError):
    'Missing local settings file'
    pass

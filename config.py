import ujson
import os

from typing import Dict

# set xen credentials
def get_xen_clusters() -> Dict:
    from core import XenXenXenSeCore

    xen_clusters = {}
    if os.path.isfile("config.json"):
        with open("config.json", "r") as config_file:
            xen_clusters = ujson.load(config_file)["xen_clusters"]
        config_file.close()

    # Docker check
    if XenXenXenSeCore.is_docker():
        if "xen_clusters" in XenXenXenSeCore.get_docker_config():
            xen_clusters = XenXenXenSeCore.get_docker_config()["xen_clusters"]

    return xen_clusters


def get_mysql_credentials() -> Dict:
    from core import XenXenXenSeCore

    mysql_credentials = {}

    if os.path.isfile("config.json"):
        with open("config.json", "r") as config_file:
            mysql_credentials = ujson.load(config_file)["mysql_credentials"]
        config_file.close()

    # Docker check
    if XenXenXenSeCore.is_docker():
        if "mysql_credentials" in XenXenXenSeCore.get_docker_config():
            mysql_credentials = XenXenXenSeCore.get_docker_config()[
                "mysql_credentials"
            ]

    return mysql_credentials


mysql_update_rate = 60 * 1
mysql_host_update_rate = 20

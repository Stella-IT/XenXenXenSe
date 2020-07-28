import ujson

# set xen credentials
def get_xen_clusters():

    from core import XenXenXenSeCore

    config_file = open("config.json", "r")
    xen_clusters = ujson.load(config_file)['xen_clusters']
    config_file.close()

    # Docker check
    if XenXenXenSeCore.is_docker():
        if "xen_clusters" in XenXenXenSeCore.get_docker_config():
            xen_clusters = XenXenXenSeCore.get_docker_config()['xen_clusters']

    return xen_clusters

def get_mysql_credentials():

    from core import XenXenXenSeCore

    config_file = open("config.json", "r")
    mysql_credentials = ujson.load(config_file)['mysql_credentials']
    config_file.close()

     # Docker check
    if XenXenXenSeCore.is_docker():
        if "mysql_credentials" in XenXenXenSeCore.get_docker_config():
            mysql_credentials = XenXenXenSeCore.get_docker_config()['mysql_credentials']

    return mysql_credentials

mysql_update_rate = 60 * 1
mysql_host_update_rate = 20

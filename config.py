import ujson

# set xen credentials
def get_xen_clusters():

    from core import XenXenXenSeCore

    config_file = open("config.json", "r")
    xen_clusters = ujson.load(config_file)['xen_clusters']
    config_file.close()

    # Docker check
    if XenXenXenSeCore.is_docker():
        xen_clusters = XenXenXenSeCore.get_docker_xen_credentials()

    return xen_clusters

def get_mysql_credentials():

    from core import XenXenXenSeCore

    config_file = open("config.json", "r")
    mysql_credentials = ujson.load(config_file)['mysql_credentials']
    config_file.close()

    mysql_credentials = mysql_credentials if XenXenXenSeCore.get_docker_mysql_credentials() is None else XenXenXenSeCore.get_docker_mysql_credentials()

    return mysql_credentials

mysql_update_rate = 60 * 1
mysql_host_update_rate = 20

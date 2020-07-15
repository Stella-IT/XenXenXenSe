# The Glorious Config File

# set xen credentials
xen_credentials = {
    "cluster-name": {
        "host": "http://your-cluster-hostname",
        "username": "im-groot",
        "password": "my-password"
    }
}

# mysql server credentials for caching.
# set it to None if you don't need it.
mysql_credentials = {
    "host": "your-mysql-host",
    "port": 3306,
    "user": "your-username",
    "password": "your-lovely-password",
    "db": "your-db-name",
    "charset": "utf8mb4"
}

mysql_update_rate = 60 * 1
mysql_host_update_rate = 20

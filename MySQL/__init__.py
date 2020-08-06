import pymysql
import schedule
import databases
import sqlalchemy
import datetime


from .interface import credentials_interface
from sqlalchemy.dialects.mysql import MEDIUMTEXT, VARCHAR, DATETIME, TEXT, FLOAT, BIGINT
from sqlalchemy import INT
from config import mysql_host_update_rate
from config import mysql_update_rate
from MySQL.Status import status

from config import get_xen_clusters, get_mysql_credentials


class DatabaseCore:
    def __init__(self):
        self.mysql_credentials: dict = get_mysql_credentials()

    def database_connection_url(self) -> str:
        if status.get_enabled():
            print("MySQL Sync: Terminating Multiple Initialization")
            raise

        if self.mysql_credentials is None:
            print("MySQL Sync: MySQL Caching is disabled!")
            raise

        cred = credentials_interface(**self.mysql_credentials)

        url = f"mysql://{cred.user}:{cred.password}@{cred.host}:{str(cred.port)}/{cred.db}"
        return url

    @property
    def metadata(self):
        return sqlalchemy.MetaData()

    @property
    def database(self):
        DATABASE_URL = self.database_connection_url()
        return databases.Database(DATABASE_URL)

    @property
    def create_engine(self):
        DATABASE_URL = self.database_connection_url()
        engine = sqlalchemy.create_engine(DATABASE_URL)
        return engine


class DatabaseManager(DatabaseCore):
    def __init__(self):
        super().__init__()
        self.database_core = self

    def hosts_table(self):
        """
        CREATE TABLE IF NOT EXISTS `hosts` (
           `cluster_id` VARCHAR(255) NOT NULL,
           `host_uuid` VARCHAR(255) NOT NULL,
           `lastUpdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
           `cpu` TEXT NOT NULL,
           `cpu_speed` FLOAT NOT NULL,
           `free_memory` BIGINT NOT NULL,
           `memory` BIGINT NOT NULL
        );
        """
        hosts = sqlalchemy.Table(
            "hosts",
            self.database_core.metadata,
            sqlalchemy.Column("cluster_id", VARCHAR(255), nullable=False),
            sqlalchemy.Column("host_uuid", VARCHAR(255), nullable=False),
            sqlalchemy.Column(
                "lastUpdate", DATETIME, nullable=False, default=datetime.datetime.utcnow
            ),
            sqlalchemy.Column("cpu", TEXT, nullable=False),
            sqlalchemy.Column("cpu_speed", FLOAT, nullable=False),
            sqlalchemy.Column("free_memory", BIGINT, nullable=False),
            sqlalchemy.Column("memory", BIGINT, nullable=False),
        )
        return hosts

    def vms_table(self):
        """
        CREATE TABLE IF NOT EXISTS `vms` (
           `cluster_id` VARCHAR(255) NOT NULL,
           `vm_uuid` VARCHAR(255) NOT NULL,
           `lastUpdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
           `name` TEXT NOT NULL,
           `description` MEDIUMTEXT NOT NULL,
           `memory` BIGINT NOT NULL,
           `vCPUs` INT NOT NULL,
           `power` TEXT NOT NULL
        );
        """
        vms = sqlalchemy.Table(
            "vms",
            self.database_core.metadata,
            sqlalchemy.Column("cluster_id", VARCHAR(255), nullable=False),
            sqlalchemy.Column("vm_uuid", VARCHAR(255), nullable=False),
            sqlalchemy.Column(
                "lastUpdate", DATETIME, nullable=False, default=datetime.datetime.utcnow
            ),
            sqlalchemy.Column("name", TEXT, nullable=False),
            sqlalchemy.Column("description", MEDIUMTEXT, nullable=False),
            sqlalchemy.Column("memory", BIGINT, nullable=False),
            sqlalchemy.Column("vCPUs", INT, nullable=False),
            sqlalchemy.Column("power", TEXT, nullable=False),
        )
        return vms

    def is_not_generated_table(self):
        metadata = self.database_core.metadata
        sqlalchemy.Table(
            self.hosts_table,
            metadata,
            sqlalchemy.Column("cluster_id", VARCHAR(255), nullable=False),
            sqlalchemy.Column("host_uuid", VARCHAR(255), nullable=False),
            sqlalchemy.Column(
                "lastUpdate", DATETIME, nullable=False, default=datetime.datetime.utcnow
            ),
            sqlalchemy.Column("cpu", TEXT, nullable=False),
            sqlalchemy.Column("cpu_speed", FLOAT, nullable=False),
            sqlalchemy.Column("free_memory", BIGINT, nullable=False),
            sqlalchemy.Column("memory", BIGINT, nullable=False),
        )
        sqlalchemy.Table(
            self.vms_table,
            metadata,
            sqlalchemy.Column("cluster_id", VARCHAR(255), nullable=False),
            sqlalchemy.Column("host_uuid", VARCHAR(255), nullable=False),
            sqlalchemy.Column(
                "lastUpdate", DATETIME, nullable=False, default=datetime.datetime.utcnow
            ),
            sqlalchemy.Column("cpu", TEXT, nullable=False),
            sqlalchemy.Column("cpu_speed", FLOAT, nullable=False),
            sqlalchemy.Column("free_memory", BIGINT, nullable=False),
            sqlalchemy.Column("memory", BIGINT, nullable=False),
        )
        metadata.create_all()


# =========================================


def sync_mysql_host_database():
    if status.get_enabled():
        print()
        print("MySQL Sync: MySQL Host Sync Triggered!")

        from XenXenXenSe.session import create_session
        from XenXenXenSe.Host import Host
        from XenXenXenSe.VM import VM
        from .Host import XenHost
        from .VM import XenVm

        for cluster_id in get_xen_clusters():
            session = create_session(cluster_id)

            # ==================================

            hosts = Host.list_host(session)
            for host in hosts:
                XenHost.update(cluster_id, host)

            XenHost.remove_orphaned(cluster_id)

        print("MySQL Sync: MySQL Host Sync Completed!")
        print()


# =========================================


def sync_mysql_database():
    if status.get_enabled():
        print()
        print("MySQL Sync: MySQL Sync Triggered!")

        from .VM import XenVm
        from .Host import XenHost
        from XenXenXenSe.VM import VM
        from XenXenXenSe.Host import Host
        from XenXenXenSe.session import create_session

        for cluster_id in get_xen_clusters():
            session = create_session(cluster_id)

            # ==================================

            print("MySQL Sync: MySQL Host Sync Triggered!")
            hosts = Host.list_host(session)
            for host in hosts:
                host.update(cluster_id, host)

            XenHost.remove_orphaned(cluster_id)

            # ===================================

            print("MySQL Sync: MySQL VM Sync Triggered!")
            vms = VM.list_vm(session)
            for _vm in vms:
                XenVm.update(cluster_id, _vm)

            XenVm.remove_orphaned(cluster_id)

        print("MySQL Sync: MySQL Sync Completed!")
        print()


# =========================================


def init_connection():
    if status.get_enabled():
        print("MySQL Sync: Terminating Multiple Initialization")
        return

    mysql_credentials = get_mysql_credentials()

    if mysql_credentials is None:
        print("MySQL Sync: MySQL Caching is disabled!")
        return

    print()
    try:
        _mysql = DatabaseManager()
        _mysql.is_not_generated_table()

        status.set_enabled(True)

        schedule.every(mysql_host_update_rate).seconds.do(sync_mysql_host_database)
        schedule.every(mysql_update_rate).seconds.do(sync_mysql_database)

        print("MySQL Sync: MySQL Caching is enabled!")

    except Exception as e:
        print("Database generation failed.", e)


# =========================================

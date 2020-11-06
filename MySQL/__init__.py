import asyncio
import datetime
from typing import Optional, no_type_check

import databases
import schedule
import sqlalchemy
from sqlalchemy import INT
from sqlalchemy.dialects.mysql import (BIGINT, DATETIME, FLOAT, MEDIUMTEXT,
                                       TEXT, VARCHAR)
from sqlalchemy.engine import Engine

from app.settings import Settings
from MySQL.interface import credentials_interface
from MySQL.Status import status


class DatabaseCore:
    def __init__(self) -> None:
        self.mysql_credentials: dict = Settings.get_mysql_credentials()

    def database_connection_url(self) -> Optional[str]:
        if status.get_enabled():
            print("MySQL Sync: Terminating Multiple Initialization")
            return None

        if self.mysql_credentials is None:
            return None

        cred = credentials_interface(**self.mysql_credentials)

        url = f"mysql://{cred.user}:{cred.password}@{cred.host}:{str(cred.port)}/{cred.db}"
        return url

    @no_type_check
    def metadata(self):
        return sqlalchemy.MetaData()

    @no_type_check
    def database(self):
        DATABASE_URL = self.database_connection_url()
        return databases.Database(DATABASE_URL)

    @property
    def create_engine(self) -> Engine:
        DATABASE_URL = self.database_connection_url()
        engine = sqlalchemy.create_engine(DATABASE_URL)
        return engine


class DatabaseManager(DatabaseCore):
    def __init__(self) -> None:
        super(DatabaseManager, self).__init__()
        self.database_core = self

    def hosts_table(self) -> sqlalchemy.Table:
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
                "lastUpdate",
                DATETIME,
                nullable=False,
                default=datetime.datetime.utcnow,
            ),
            sqlalchemy.Column("cpu", TEXT, nullable=False),
            sqlalchemy.Column("cpu_speed", FLOAT, nullable=False),
            sqlalchemy.Column("free_memory", BIGINT, nullable=False),
            sqlalchemy.Column("memory", BIGINT, nullable=False),
        )
        return hosts

    def vms_table(self) -> sqlalchemy.Table:
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
                "lastUpdate",
                DATETIME,
                nullable=False,
                default=datetime.datetime.utcnow,
            ),
            sqlalchemy.Column("name", TEXT, nullable=False),
            sqlalchemy.Column("description", MEDIUMTEXT, nullable=False),
            sqlalchemy.Column("memory", BIGINT, nullable=False),
            sqlalchemy.Column("vCPUs", INT, nullable=False),
            sqlalchemy.Column("power", TEXT, nullable=False),
        )
        return vms

    async def is_not_generated_table(self) -> None:
        hosts_table = """CREATE TABLE IF NOT EXISTS `hosts` (
                  `cluster_id` VARCHAR(255) NOT NULL,
                  `host_uuid` VARCHAR(255) NOT NULL,
                  `lastUpdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `cpu` TEXT NOT NULL,
                  `cpu_speed` FLOAT NOT NULL,
                  `free_memory` BIGINT NOT NULL,
                  `memory` BIGINT NOT NULL  
        );"""
        vms_table = """CREATE TABLE IF NOT EXISTS `vms` (
                   `cluster_id` VARCHAR(255) NOT NULL,
                   `vm_uuid` VARCHAR(255) NOT NULL,
                   `lastUpdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   `name` TEXT NOT NULL,
                   `description` MEDIUMTEXT NOT NULL,
                   `memory` BIGINT NOT NULL,
                   `vCPUs` INT NOT NULL,
                   `power` TEXT NOT NULL
        );"""

        if not self.create_engine.has_table(
            "hosts"
        ) or self.create_engine.has_table("vms"):
            self.create_engine.execute(hosts_table)
            self.create_engine.execute(vms_table)


# =========================================


async def sync_mysql_host_database() -> None:
    if status.get_enabled():
        print()
        print("MySQL Sync: MySQL Host Sync Triggered!")

        from XenGarden.Host import Host
        from XenGarden.session import create_session

        from .Host import XenHost

        for cluster_id in Settings.get_xen_clusters():
            session = create_session(cluster_id, Settings.get_xen_clusters())

            # ==================================

            hosts = Host.list_host(session)
            for host in hosts:
                await XenHost().update(cluster_id, host)

            await XenHost().remove_orphaned(cluster_id)

        print("MySQL Sync: MySQL Host Sync Completed!")
        print()


# =========================================


async def sync_mysql_database() -> None:
    if status.get_enabled():
        print()
        print("MySQL Sync: MySQL Sync Triggered!")

        from XenGarden.Host import Host
        from XenGarden.session import create_session
        from XenGarden.VM import VM

        from .Host import XenHost
        from .VM import XenVm

        for cluster_id in Settings.get_xen_clusters():
            session = create_session(cluster_id, Settings.get_xen_clusters())

            # ==================================

            print("MySQL Sync: MySQL Host Sync Triggered!")
            hosts = Host.list_host(session)
            for host in hosts:
                host.update(cluster_id, host)

            await XenHost().remove_orphaned(cluster_id)

            # ===================================

            print("MySQL Sync: MySQL VM Sync Triggered!")
            vms = VM.list_vm(session)
            for _vm in vms:
                await XenVm().update(cluster_id, _vm)

            await XenVm().remove_orphaned(cluster_id)
        print("MySQL Sync: MySQL Sync Completed!")
        print()


# =========================================


class CoreInitialization(DatabaseManager):
    def __init__(self) -> None:
        super(CoreInitialization, self).__init__()

    async def init_connection(self) -> None:
        if status.get_enabled():
            print("MySQL Sync: Terminating Multiple Initialization")
            return

        mysql_credentials = Settings.get_mysql_credentials()

        if mysql_credentials is None:
            print("MySQL Sync: MySQL Caching is disabled!")
            return

        print()
        if not self.create_engine.has_table(
            "hosts"
        ) or self.create_engine.has_table("vms"):
            try:
                await self.is_not_generated_table()
            except Exception as e:
                print("Database generation failed.", e)
                return


def init_connection() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        mysql_update_rate = 60 * 1
        mysql_host_update_rate = 20
        # generate MySQL database table
        schedule.every(mysql_host_update_rate).seconds.do(
            loop.call_soon_threadsafe, sync_mysql_host_database
        )
        schedule.every(mysql_update_rate).seconds.do(
            loop.call_soon_threadsafe, sync_mysql_database
        )
        print("MySQL Sync: MySQL Caching is enabled!")
    except Exception as e:
        print("Database generation failed.", e)

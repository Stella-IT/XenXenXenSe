import pymysql
import schedule

from config import mysql_credentials, mysql_update_rate, mysql_host_update_rate
from .Status import status


# =========================================


def sync_mysql_host_database():
    if status.get_enabled():
        print()
        print("MySQL Sync: MySQL Host Sync Triggered!")

        from config import xen_credentials
        from XenXenXenSe.session import create_session
        from XenXenXenSe.Host import Host
        from XenXenXenSe.VM import VM
        from .Host import host
        from .VM import vm

        for cluster_id in xen_credentials:
            session = create_session(cluster_id)

            # ==================================

            hosts = Host.list_host(session)
            for _host in hosts:
                host.update_host(cluster_id, _host)

            host.remove_orphaned_host(cluster_id)

        print("MySQL Sync: MySQL Host Sync Completed!")
        print()


# =========================================


def sync_mysql_database():
    if status.get_enabled():
        print()
        print("MySQL Sync: MySQL Sync Triggered!")

        from config import xen_credentials
        from XenXenXenSe.session import create_session
        from XenXenXenSe.Host import Host
        from XenXenXenSe.VM import VM
        from .Host import host
        from .VM import vm

        for cluster_id in xen_credentials:
            session = create_session(cluster_id)

            # ==================================

            print("MySQL Sync: MySQL Host Sync Triggered!")
            hosts = Host.list_host(session)
            for host in hosts:
                host.update_host(cluster_id, host)

            host.remove_orphaned_host(cluster_id)

            # ===================================

            print("MySQL Sync: MySQL VM Sync Triggered!")
            vms = VM.list_vm(session)
            for _vm in vms:
                vm.update_vm(cluster_id, _vm)

            vm.remove_orphaned_vm(cluster_id)

        print("MySQL Sync: MySQL Sync Completed!")
        print()


# =========================================

def init_connection():
    if status.get_enabled():
        print("MySQL Sync: Terminating Multiple Initialization")
        return

    if mysql_credentials is None:
        print("MySQL Sync: MySQL Caching is disabled!")
        return

    print()
    try:
        connection = pymysql.connect(**mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            sql = '''CREATE TABLE 
                IF NOT EXISTS `hosts` (
                  `cluster_id` VARCHAR(255) NOT NULL,
                  `host_uuid` VARCHAR(255) NOT NULL,
                  `lastUpdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `cpu` TEXT NOT NULL,
                  `cpu_speed` FLOAT NOT NULL,
                  `free_memory` BIGINT NOT NULL,
                  `memory` BIGINT NOT NULL  
                );'''
            cursor.execute(sql)
            sql = '''CREATE TABLE
                 IF NOT EXISTS `vms` (
                   `cluster_id` VARCHAR(255) NOT NULL,
                   `vm_uuid` VARCHAR(255) NOT NULL,
                   `lastUpdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                   `name` TEXT NOT NULL,
                   `description` MEDIUMTEXT NOT NULL,
                   `memory` BIGINT NOT NULL,
                   `vCPUs` INT NOT NULL,
                   `power` TEXT NOT NULL
                 );'''
            cursor.execute(sql)

        connection.commit()

        connection.close()
        status.set_enabled(True)

        schedule.every(mysql_host_update_rate).seconds.do(sync_mysql_host_database)
        schedule.every(mysql_update_rate).seconds.do(sync_mysql_database)

        print("MySQL Sync: MySQL Caching is enabled!")

    except Exception as e:
        print("Database generation failed.", e)

# =========================================

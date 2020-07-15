import pymysql
from XenXenXenSe.Host import Host

from config import mysql_credentials
from MySQL.Status import status


class host:
    sql = ""

    @classmethod
    def update_host(cls, cluster_id, host: Host):

        if host is None:
            print("nope")
            return

        if status.get_enabled():
            try:
                connection = pymysql.connect(**mysql_credentials, cursorclass=pymysql.cursors.DictCursor)
                uuid = host.get_uuid()

                with connection.cursor() as cursor:
                    cls.sql = "SELECT * FROM `hosts` WHERE `cluster_id`=%s AND `host_uuid`=%s"
                    cursor.execute(cls.sql, (cluster_id, uuid))

                    cpu_info = host.get_cpu_info()

                    cpu = cpu_info['modelname']
                    speed = float(cpu_info['speed'])
                    free_memory = int(host.get_free_memory())
                    memory = int(host.get_total_memory())

                    if cursor.rowcount == 0:
                        cls.sql = "INSERT INTO `hosts` (`cluster_id`, `host_uuid`, `cpu`, `cpu_speed`, `free_memory`, `memory`) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(cls.sql, (cluster_id, uuid, cpu, speed, free_memory, memory))

                    else:
                        host_data = cursor.fetchone()

                        is_different = (
                                host_data['cpu'] != cpu or
                                host_data['cpu_speed'] != speed or
                                host_data['free_memory'] != free_memory or
                                host_data['memory'] != memory
                        )

                        if is_different:
                            cls.sql = "UPDATE `hosts` SET `lastUpdate`=NOW(), `cpu`=%s, `cpu_speed`=%s, `free_memory`=%s, `memory`=%s WHERE `cluster_id`=%s AND `host_uuid`=%s"
                            cursor.execute(cls.sql, (cpu, speed, free_memory, memory, cluster_id, uuid))
                        else:
                            sql = "UPDATE `hosts` SET `lastUpdate`=NOW() WHERE `cluster_id`=%s AND `host_uuid`=%s"
                            cursor.execute(cls.sql, (cluster_id, uuid))

                connection.commit()
            except Exception as e:
                print("MySQL Sync: update_host failed.", e, cls.sql)

    @classmethod
    def remove_orphaned_host(cls, cluster_id):
        if status.get_enabled():
            try:
                connection = pymysql.connect(**mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

                with connection.cursor() as cursor:
                    from XenXenXenSe.session import create_session

                    cls.sql = "SELECT * FROM `hosts`"
                    cursor.execute(cls.sql)

                    result = cursor.fetchall()

                    for host_v in result:
                        cluster_id = host_v['cluster_id']
                        host_uuid = host_v['host_uuid']

                        session = create_session(cluster_id)
                        host = Host.get_by_uuid(session, host_uuid)

                        if host is None:
                            cls.sql = "DELETE FROM `hosts` WHERE `cluster_id`=%s AND `host_uuid`=%s"
                            cursor.execute(cls.sql, (cluster_id, host_uuid))

                connection.commit()
            except Exception as e:
                print("MySQL Sync: remove_orphaned_host failed.", e)

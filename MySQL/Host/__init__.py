from XenXenXenSe.Host import Host

from MySQL.Status import status
from MySQL import DatabaseCore


class XenHost(DatabaseCore):
    def __init__(self):
        super().__init__()
        self.sql = ""

    def update(self, cluster_id, _host: Host):

        if _host is None:
            print("nope")
            return

        if status.get_enabled():
            try:
                uuid = _host.get_uuid()
                self.sql = (
                    "SELECT * FROM `hosts` WHERE `cluster_id`=%s AND `host_uuid`=%s"
                )
                low_count = await self.database.execute(self.sql, (cluster_id, uuid))

                cpu_info = _host.get_cpu_info()

                cpu = cpu_info["modelname"]
                speed = float(cpu_info["speed"])
                free_memory = int(_host.get_free_memory())
                memory = int(_host.get_total_memory())

                if low_count == 0:
                    self.sql = (
                        "INSERT INTO `hosts` (`cluster_id`, `host_uuid`, `cpu`,"
                        " `cpu_speed`, `free_memory`, `memory`) VALUES (%s, %s, %s,"
                        " %s, %s, %s)"
                    )
                    await self.database.execute(
                        self.sql, (cluster_id, uuid, cpu, speed, free_memory, memory)
                    )

                else:
                    host_data = await self.database.fetch_one()
                    is_different = (
                        host_data["cpu"] != cpu
                        or host_data["cpu_speed"] != speed
                        or host_data["free_memory"] != free_memory
                        or host_data["memory"] != memory
                    )

                    if is_different:
                        self.sql = (
                            "UPDATE `hosts` SET `lastUpdate`=NOW(), `cpu`=%s,"
                            " `cpu_speed`=%s, `free_memory`=%s, `memory`=%s WHERE"
                            " `cluster_id`=%s AND `host_uuid`=%s"
                        )
                        await self.database.execute(
                            self.sql,
                            (cpu, speed, free_memory, memory, cluster_id, uuid),
                        )
                    else:
                        self.sql = (
                            "UPDATE `hosts` SET `lastUpdate`=NOW() WHERE"
                            " `cluster_id`=%s AND `host_uuid`=%s"
                        )
                        await self.database.execute(self.sql, (cluster_id, uuid))

            except Exception as e:
                print("MySQL Sync: update failed.", e, self.sql)

    def remove_orphaned(self, cluster_id):
        if status.get_enabled():
            try:
                from XenXenXenSe.session import create_session

                self.sql = "SELECT * FROM `hosts`"
                await self.database.execute(self.sql)

                result = await self.database.fetch_all()

                for host_v in result:
                    cluster_id = host_v["cluster_id"]
                    host_uuid = host_v["host_uuid"]

                    session = create_session(cluster_id)
                    _host = Host.get_by_uuid(session, host_uuid)

                    if _host is None:
                        self.sql = (
                            "DELETE FROM `hosts` WHERE `cluster_id`=%s AND"
                            " `host_uuid`=%s"
                        )
                        await self.database.execute(self.sql, (cluster_id, host_uuid))
            except Exception as e:
                print("MySQL Sync: remove_orphaned failed.", e)

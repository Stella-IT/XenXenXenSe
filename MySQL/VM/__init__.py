from XenXenXenSe.VM import VM

from MySQL.Status import status
from MySQL import DatabaseCore


class XenVm(DatabaseCore):
    def __init__(self):
        super().__init__()
        self.sql = ""

    async def update(self, cluster_id, _vm: VM):
        if _vm is None:
            print("nope")
            return

        if status.get_enabled():
            try:
                uuid = _vm.get_uuid()
                self.sql = "SELECT * FROM `vms` WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                low_count = await self.database.execute(
                    self.sql, (cluster_id, uuid)
                )

                vCPUs = int(_vm.get_vCPUs())
                memory = int(_vm.get_memory())
                name = _vm.get_name()
                description = _vm.get_description()
                power = _vm.get_power_state()
                if low_count == 0:

                    self.sql = "INSERT INTO `vms` (`cluster_id`, `vm_uuid`, `vCPUs`, `memory`, `name`, `description`, `power`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    await self.database.execute(
                        self.sql,
                        (
                            cluster_id,
                            uuid,
                            vCPUs,
                            memory,
                            name,
                            description,
                            power,
                        ),
                    )
                else:
                    vm_data = await self.database.fetch_one()
                    is_different = (
                        int(vm_data["vCPUs"]) != vCPUs
                        or int(vm_data["memory"]) != memory
                        or vm_data["name"] != name
                        or vm_data["description"] != description
                        or vm_data["power"] != power
                    )
                    if is_different:
                        self.sql = "UPDATE `vms` SET `lastUpdate`=NOW(), `vCPUs`=%s, `memory`=%s, `name`=%s, `description`=%s, `power`=%s WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                        await self.database.execute(
                            self.sql,
                            (
                                vCPUs,
                                memory,
                                name,
                                description,
                                power,
                                cluster_id,
                                uuid,
                            ),
                        )

                    else:
                        self.sql = "UPDATE `vms` SET `lastUpdate`=NOW() WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                        await self.database.execute(
                            self.sql, (cluster_id, uuid)
                        )
            except Exception as e:
                print("MySQL Sync: update failed.", e, "\n", self.sql)

    async def remove_orphaned(self, cluster_id):
        if status.get_enabled():
            try:
                from XenXenXenSe.session import create_session

                self.sql = "SELECT * FROM `vms`"
                await self.database.execute(self.sql)

                result = await self.database.fetch_all()

                for vm_v in result:
                    cluster_id = vm_v["cluster_id"]
                    vm_uuid = vm_v["vm_uuid"]
                    print(cluster_id, vm_uuid)

                    session = create_session(cluster_id)
                    _vm = VM.get_by_uuid(session, vm_uuid)

                    if _vm is None:
                        self.sql = "DELETE FROM `vms` WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                        await self.database.execute(
                            self.sql, (cluster_id, vm_uuid)
                        )

            except Exception as e:
                print("MySQL Sync: remove_orphaned failed.", e)

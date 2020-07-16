import pymysql
from XenXenXenSe.VM import VM

from config import mysql_credentials
from MySQL.Status import status


class vm:
    sql = ""

    @classmethod
    def update_vm(cls, cluster_id, vm: VM):
        if vm is None:
            print("nope")
            return

        if status.get_enabled():
            try:
                connection = pymysql.connect(**mysql_credentials, cursorclass=pymysql.cursors.DictCursor)
                uuid = vm.get_uuid()

                with connection.cursor() as cursor:
                    cls.sql = "SELECT * FROM `vms` WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                    cursor.execute(cls.sql, (cluster_id, uuid))

                    vCPUs = int(vm.get_vCPUs())
                    memory = int(vm.get_memory())
                    name = vm.get_name()
                    description = vm.get_description()
                    power = vm.get_power_state()

                    if cursor.rowcount == 0:
                        cls.sql = "INSERT INTO `vms` (`cluster_id`, `vm_uuid`, `vCPUs`, `memory`, `name`, `description`, `power`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(cls.sql, (cluster_id, uuid, vCPUs, memory, name, description, power))

                    else:
                        vm_data = cursor.fetchone()

                        is_different = (
                                int(vm_data['vCPUs']) != vCPUs or
                                int(vm_data['memory']) != memory or
                                vm_data['name'] != name or
                                vm_data['description'] != description or
                                vm_data['power'] != power
                        )

                        if is_different:
                            cls.sql = "UPDATE `vms` SET `lastUpdate`=NOW(), `vCPUs`=%s, `memory`=%s, `name`=%s, `description`=%s, `power`=%s WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                            cursor.execute(cls.sql, (vCPUs, memory, name, description, power, cluster_id, uuid))

                        else:
                            cls.sql = "UPDATE `vms` SET `lastUpdate`=NOW() WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                            cursor.execute(cls.sql, (cluster_id, uuid))

                connection.commit()
            except Exception as e:
                print("MySQL Sync: update_vm failed.", e, "\n", cls.sql)

    @classmethod
    def remove_orphaned_vm(cls, cluster_id):
        if status.get_enabled():
            try:
                connection = pymysql.connect(**mysql_credentials, cursorclass=pymysql.cursors.DictCursor)

                with connection.cursor() as cursor:
                    from XenXenXenSe.session import create_session

                    cls.sql = "SELECT * FROM `vms`"
                    cursor.execute(cls.sql)

                    result = cursor.fetchall()

                    for vm_v in result:
                        cluster_id = vm_v['cluster_id']
                        vm_uuid = vm_v['vm_uuid']
                        print(cluster_id, vm_uuid)

                        session = create_session(cluster_id)
                        vm = VM.get_by_uuid(session, vm_uuid)

                        if vm is None:
                            cls.sql = "DELETE FROM `vms` WHERE `cluster_id`=%s AND `vm_uuid`=%s"
                            cursor.execute(cls.sql, (cluster_id, vm_uuid))

                connection.commit()
            except Exception as e:
                print("MySQL Sync: remove_orphaned_vm failed.", e)

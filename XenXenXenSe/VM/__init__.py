from XenXenXenSe.Console import Console
from XenXenXenSe.GuestMetrics import GuestMetrics

class VM():
    """ The Virtual Machine Object """

    def __init__(self, session, vm):
        self.session = session
        self.vm = vm

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns VM object that has specific uuid """
        try:
            vm = session.xenapi.VM.get_by_uuid(uuid)

            if vm is not None:
                return VM(session, vm)
            else:
                return None
        except Exception as e:
            print("VM.get_by_uuid Exception", e)
            return None

    @staticmethod
    def list_templates(session):
        """ gets Templates available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of VM object)"""
        try:
            allTemplates = []
            allVMs = session.xenapi.VM.get_all_records()

            for vmF in allVMs:
                template = VM(session, vmF)

                if template.is_template():
                    allTemplates.append(template)

            return allTemplates
        except Exception as e:
            print("VM.get_templates Exception", e)
            return None

    @staticmethod
    def list_vm(session):
        """ gets VMs available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of VM object)"""
        try:
            allVMList = []
            allVMs = session.xenapi.VM.get_all()

            for vmF in allVMs:
                vm = VM(session, vmF)
                if not vm.is_template():
                    allVMList.append(vm)

            return allVMList
        except Exception as e:
            print("VM.list_vm Exception", e)
            return None

    def get_uuid(self):
        """ get UUID of VM """
        try:
            return self.session.xenapi.VM.get_uuid(self.vm)
        except Exception as e:
            print("VM.get_uuid Exception", e)
            return None

    def is_template(self):
        """ Returns rather this vm is template """
        try:
            return self.session.xenapi.VM.get_is_a_template(self.vm)
        except Exception as e:
            print("VM.get_uuid Exception", e)
            return None

    def serialize(self):
        """ Returns Info for of the VM """
        return {
            "name": self.get_name(),
            "bios": self.get_bios_strings(),
            "power": self.get_power_state(),
            "description": self.get_description(),
            "uuid": self.get_uuid(),
            "vCPUs": self.get_vCPUs(),
            "memory": self.get_memory(),
        }

    def get_power_state(self):
        """ Returns Power State of the VM """
        try:
            return self.session.xenapi.VM.get_power_state(self.vm)
        except Exception as e:
            print("VM.get_power_state Exception", e)
            return None

    def get_consoles(self):
        """ Returns Consoles of the VM """
        try:
            consoles = self.session.xenapi.VM.get_consoles(self.vm)

            consoleList = []
            for console in consoles:
                consoleList.append(Console(self.session, console))
            return consoleList
        except Exception as e:
            print("VM.get_consoles Exception", e)
            return None

    def get_guest_metrics(self):
        """ Returns Guest Metrics Object of the VM """
        try:
            return GuestMetrics(self.session, self.session.xenapi.VM.get_guest_metrics(self.vm))
        except Exception as e:
            print("VM.get_guest_metrics Exception", e)
            return None

    def get_snapshots(self):
        """ Returns Available Snapshots (List of VM object) """
        try:
            allSnapshots = []
            snapshots = self.session.xenapi.VM.get_snapshots(self.vm)

            for snapshotNo in snapshots:
                allSnapshots.append(VM(self.session, snapshots[snapshotNo]))

            return allSnapshots
        except Exception as e:
            print("VM.get_snapshots Exception", e)
            return None

    def get_name(self):
        """ Returns VM's XenServer Name """
        try:
            return self.session.xenapi.VM.get_name_label(self.vm)
        except Exception as e:
            print("VM.get_name Exception", e)
            return False
        #
        return True

    def get_description(self):
        """ Returns VM's XenServer Description """
        try:
            return self.session.xenapi.VM.get_name_description(self.vm)
        except Exception as e:
            print("VM.get_description Exception", e)
            return False
        #
        return True

    def start(self):
        """ Starts VM (Returns Boolean, True: Success, False: Fail) """
        try:
            self.session.xenapi.VM.start(self.vm, False, False)
        except Exception as e:
            print("VM.start Exception", e)
            return False

        return True

    def shutdown(self):
        """ Shutdowns VM (Returns Boolean, True: Success, False: Fail) """
        try:
            self.session.xenapi.VM.clean_shutdown(self.vm)
        except Exception as e:
            print("VM.shutdown Exception", e)
            return False

        return True

    def force_shutdown(self):
        """ Force Shutdown VM (Returns Boolean, True: Success, False: Fail) """
        try:
            self.session.xenapi.VM.hard_shutdown(self.vm)
        except Exception as e:
            print("VM.force_shutdown Exception", e)
            return False

        return True

    def reboot(self):
        """ Reboot VM (Returns Boolean, True: Success, False: Fail) """
        try:
            self.session.xenapi.VM.clean_reboot(self.vm)
        except Exception as e:
            print("VM.reboot Exception", e)
            return False

        return True

    def force_reboot(self):
        """ Force Reboot VM (Returns Boolean, True: Success, False: Fail) """
        try:
            self.session.xenapi.VM.hard_reboot(self.vm)
        except Exception as e:
            print("VM.force_reboot Exception", e)
            return False

        return True

    def snapshot(self, snapshot_name):
        """ Take a snapshot of current VM """
        try:
            self.session.xenapi.VM.snapshot(self.vm, snapshot_name)
        except Exception as e:
            print("VM.snapshot Exception", e)
            return False

        return True

    def suspend(self):
        try:
            self.session.xenapi.VM.suspend(self.vm)
        except Exception as e:
            print("VM.suspend Exception", e)
            return False

        return True

    def resume(self):
        try:
            self.session.xenapi.VM.resume(self.vm, True, False)
        except Exception as e:
            print("VM.resume Exception", e)
            return False

        return True

    def pause(self):
        try:
            self.session.xenapi.VM.pause(self.vm)
        except Exception as e:
            print("VM.pause Exception", e)
            return False

        return True

    def unpause(self):
        try:
            self.session.xenapi.VM.unpause(self.vm)
        except Exception as e:
            print("VM.unpause Exception", e)
            return False

        return True

    def clone(self, new_name):
        try:
            vm = self.session.xenapi.VM.clone(self.vm, new_name)
            self.session.xenapi.VM.set_is_a_template(vm, False)
            return VM(self.session, vm)
        except Exception as e:
            print("VM.clone Exception", e)
            return False

        return True

    def set_name(self, name):
        try:
            self.session.xenapi.VM.set_name_label(self.vm, name)
        except Exception as e:
            print("VM.set_name Exception", e)
            return False
        #
        return True

    def set_description(self, description):
        try:
            self.session.xenapi.VM.set_name_description(self.vm, description)
        except Exception as e:
            print("VM.set_description Exception", e)
            return False
        #
        return True

    def set_vCPUs(self, vCPUs):
        try:
            tmp_platform = self.session.xenapi.VM.get_platform(self.vm,)
            vCPU_platform = { "cores-per-socket": str(vCPUs) }

            platform = { **tmp_platform, **vCPU_platform }

            self.session.xenapi.VM.set_platform(self.vm, platform)
            self.session.xenapi.VM.set_VCPUs_max(self.vm, vCPUs)
            self.session.xenapi.VM.set_VCPUs_at_startup(self.vm, vCPUs)
        except Exception as e:
            print("VM.set_vCPUs Exception", e)
            return False
        #
        return True

    def set_memory(self, memory):
        try:
            self.session.xenapi.VM.set_memory_limits(self.vm, memory, memory, memory, memory)
        except Exception as e:
            print("VM.set_memory Exception", e)
            return False
        #
        return True

    def get_platform(self):
        try:
            return self.session.xenapi.VM.get_platform(self.vm)
        except Exception as e:
            print("VM.get_platform Exception", e)
            return None
        #
        return None

    def set_platform(self, platform):
        try:
            return self.session.xenapi.VM.set_platform(self.vm, platform)
        except Exception as e:
            print("VM.set_platform Exception", e)
            return None
        #
        return None

    def get_vCPUs(self):
        try:
            return self.session.xenapi.VM.get_VCPUs_at_startup(self.vm)
        except Exception as e:
            print("VM.get_vCPUs Exception", e)
            return None
        #
        return None

    def get_vCPU_params(self):
        try:
            return self.session.xenapi.VM.get_VCPUs_params(self.vm)
        except Exception as e:
            print("VM.get_vCPU_params Exception", e)
            return None
        #
        return None

    def get_bios_strings(self):
        try:
            return self.session.xenapi.VM.get_bios_strings(self.vm)
        except Exception as e:
            print("VM.get_bios_strings Exception", e)
            return None
        #
        return None

    def set_bios_strings(self, input_bios_str):
        try:
            tmp_bios_str = self.session.xenapi.VM.get_bios_strings(self.vm)
            bios_str = { **tmp_bios_str, **input_bios_str }
            self.session.xenapi.VM.set_bios_strings(self.vm, bios_str)
            return True
        except Exception as e:
            print("VM.set_bios_strings Exception", e)
            return False
        #
        return None

    def get_memory(self):
        try:
            return self.session.xenapi.VM.get_memory_static_max(self.vm)
        except Exception as e:
            print("VM.get_memory Exception", e)
            return None
        #
        return None

    def delete(self):
        from XenXenXenSe.VBD import VBD

        try:
            vbds = self.get_Disks()
            for vbd in vbds:
                vbd.destroy()

            self.session.xenapi.VM.destroy(self.vm)
            return True
        except Exception as e:
            print("VM.delete Exception", e)
            return False

    def destroy(self):
        return self.delete()

    def get_VBDs(self):
        from XenXenXenSe.VBD import VBD

        try:
            vbds = self.session.xenapi.VM.get_VBDs(self.vm)

            vbd_list = []
            for vbd in vbds:
                vbd_list.append(VBD(self.session, vbd))

            return vbd_list
        except Exception as e:
            print("VM.get_VBDs Exception", e)
            return None

    def get_CDs(self):
        from XenXenXenSe.VBD import VBD

        try:
            vbds = self.session.xenapi.VM.get_VBDs(self.vm)

            vbd_list = []
            for vbd in vbds:
                thisVBD = VBD(self.session, vbd)

                if thisVBD.get_type() == "CD":
                    vbd_list.append(thisVBD)

            return vbd_list
        except Exception as e:
            print("VM.get_CDs Exception", e)
            return None

    def get_VIFs(self):
        from XenXenXenSe.VIF import VIF

        try:
            vifs = self.session.xenapi.VM.get_VIFs(self.vm)

            vif_list = []
            for vif in vifs:
                thisVIF = VIF(self.session, vif)
                vif_list.append(thisVIF)

            return vif_list
        except Exception as e:
            print("VIF.get_VIFs Exception", e)
            return None

    def get_VIF(self):
        vifs = self.get_VIFs()
        if vifs is not None:
            return vifs[0]
        else:
            return None

    def get_CD(self):
        return self.get_CDs()[0]

    def get_Disks(self):
        from XenXenXenSe.VBD import VBD

        try:

            vbds = self.session.xenapi.VM.get_VBDs(self.vm)

            vbd_list = []
            for vbd in vbds:
                thisVBD = VBD(self.session, vbd)

                if thisVBD.get_type() == "Disk":
                    vbd_list.append(thisVBD)

            return vbd_list
        except Exception as e:
            print("VM.get_Disks Exception", e)
            return None




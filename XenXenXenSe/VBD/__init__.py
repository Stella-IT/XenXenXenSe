from deprecated import deprecated

from XenXenXenSe.VDI import VDI


class VBD:
    """ The Virtual Block Device Object """

    def __init__(self, session, vbd):
        self.session = session
        self.vbd = vbd

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns SR object that has specific uuid """
        try:
            vbd = session.xenapi.VBD.get_by_uuid(uuid)

            if vbd is not None:
                return VBD(session, vbd)
            else:
                return None
        except Exception as e:
            print("VBD.get_by_uuid Exception", e)
            return None

    @staticmethod
    def get_all(session):
        """ returns VBDs existing on this _host """
        try:
            vbds = session.xenapi.VBD.get_all()
            vbd_list = []

            for vbd in vbds:
                vbd_list.append(VBD(session, vbd))

            return vbd_list
        except Exception as e:
            print("VBD.get_all Exception", e)
            return None

    @deprecated
    def serialize(self) -> dict:
        vm = self.get_VM()
        vdi = self.get_VDI()

        if vm is not None:
            vm = vm.serialize()

        if vdi is not None:
            vdi = vdi.serialize()

        return {
            "_vm": vm,
            "vdi": vdi,
            "bootable": self.get_bootable(),
            "attached": self.get_currently_attached(),
            "unpluggable": self.get_unpluggable(),
            "device": self.get_device(),
            "type": self.get_type(),
            "uuid": self.get_uuid(),
            "mode": self.get_mode(),
        }

    def get_VM(self):
        """ get VM attached to the specified VBD """
        from XenXenXenSe.VM import VM

        try:
            vm = self.session.xenapi.VBD.get_VM(self.vbd)

            if vm is not None:
                return VM(self.session, vm)
            else:
                return None
        except Exception as e:
            print("VBD.get_VM Exception", e)
            return None

    def get_VDI(self) -> VDI:
        """ get VDI attached to the specified VBD """
        try:
            vdi = self.session.xenapi.VBD.get_VDI(self.vbd)

            if vdi is not None:
                return VDI(self.session, vdi)
            else:
                return None
        except Exception as e:
            print("VBD.get_VDI Exception", e)
            return None

    def get_uuid(self) -> str:
        """ get UUID of VBD """
        try:
            return self.session.xenapi.VBD.get_uuid(self.vbd)

        except Exception as e:
            print("VBD.get_uuid Exception", e)
            return None

    def get_mode(self) -> str:
        """ get mode of VBD """
        try:
            return self.session.xenapi.VBD.get_mode(self.vbd)

        except Exception as e:
            print("VBD.get_mode Exception", e)
            return None

    def get_type(self) -> str:
        """ get type of VBD """
        try:
            return self.session.xenapi.VBD.get_type(self.vbd)

        except Exception as e:
            print("VBD.get_type Exception", e)
            return None

    def get_bootable(self) -> bool:
        """ get VBD is bootable """
        try:
            return self.session.xenapi.VBD.get_bootable(self.vbd)
        except Exception as e:
            print("VBD.get_bootable Exception", e)
            return False

    def get_currently_attached(self) -> bool:
        """ get VBD is currently attached """
        try:
            return self.session.xenapi.VBD.get_currently_attached(self.vbd)
        except Exception as e:
            print("VBD.get_currently_attached Exception", e)
            return False

    def get_unpluggable(self) -> bool:
        """ get VBD is unpluggable """
        try:
            return self.session.xenapi.VBD.get_unpluggable(self.vbd)
        except Exception as e:
            print("VBD.get_unpluggable Exception", e)
            return False

    def get_device(self) -> str:
        """ get VBD device """
        try:
            return self.session.xenapi.VBD.get_device(self.vbd)
        except Exception as e:
            print("VBD.get_device Exception", e)
            return None

    def destroy(self) -> bool:
        """ eject VDI from VBD """
        try:
            self.session.xenapi.VBD.destory(self.vbd)
            return True
        except Exception as e:
            print("VBD.destroy Exception", e)
            return False

    def insert(self, vdi: VDI) -> bool:
        """ insert VDI to VBD """
        try:
            self.session.xenapi.VBD.insert(self.vbd, vdi.vdi)
            return True
        except Exception as e:
            print("VBD.insert Exception", e)
            return False

    def eject(self) -> bool:
        """ eject VDI from VBD """
        try:
            self.session.xenapi.VBD.eject(self.vbd)
            return True
        except Exception as e:
            print("VBD.eject Exception", e)
            return False

    def plug(self) -> bool:
        """ plug specified VBD """
        try:
            self.session.xenapi.VBD.plug(self.vbd)
            return True
        except Exception as e:
            print("VBD.plug Exception", e)
            return False

    def unplug(self) -> bool:
        """ unplug VBD """
        try:
            self.session.xenapi.VBD.unplug(self.vbd)
            return True
        except Exception as e:
            print("VBD.unplug Exception", e)
            return False

    def unplug_force(self) -> bool:
        """ unplug VBD """
        try:
            self.session.xenapi.VBD.unplug_force(self.vbd)
            return True
        except Exception as e:
            print("VBD.unplug_force Exception", e)
            return False

from XenXenXenSe.GuestMetrics import GuestMetrics
from XenXenXenSe.Console import Console


class VIF:
    """ The Virtual Interface """

    def __init__(self, session, vif):
        self.session = session
        self.vif = vif

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns VIF object that has specific uuid """
        try:
            vif = session.xenapi.VIF.get_by_uuid(uuid)

            if vif is not None:
                return VIF(session, vif)
            else:
                return None
        except Exception as e:
            print("VIF.get_by_uuid Exception", e)
            return None

    @staticmethod
    def get_all(session):
        """ gets VIFs available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of VIF object)"""
        try:
            allVIFList = []
            allVIFs = session.xenapi.VIF.get_all()

            for vif in allVIFs:
                thisVif = VIF(session, vif)
                allVIFList.append(thisVif)

            return allVIFList
        except Exception as e:
            print("VIF.get_all Exception", e)
            return None

    def serialize(self) -> dict:
        """ Returns Info for of the VM """
        vm = self.get_vm()
        if vm is not None:
            vm = vm.serialize()

        return {
            "attached": self.get_attached(),
            "_vm": vm,
            "uuid": self.get_uuid(),
            "mac": self.get_mac(),
            "mtu": self.get_mtu(),
            "qos": {
                "type": self.get_qos_type(),
                "info": self.get_qos_info(),
                "supported": self.supported_qos_types()
            },
            "ipv4": {
                "address": self.get_address_v4(),
                "gateway": self.get_gateway_v4()
            },
            "ipv6": {
                "address": self.get_address_v6(),
                "gateway": self.get_gateway_v6()
            }
        }

    def get_uuid(self):
        try:
            return self.session.xenapi.VIF.get_uuid(self.vif)
        except Exception as e:
            print("VIF.get_uuid Exception", e)
            return None

    def get_attached(self):
        try:
            return self.session.xenapi.VIF.get_currently_attached(self.vif)
        except Exception as e:
            print("VIF.get_attached Exception", e)
            return False

    def get_vm(self):
        from XenXenXenSe.VM import VM

        try:
            vm = self.session.xenapi.VIF.get_VM(self.vif)

            if vm is not None:
                vm = VM(self.session, vm)
                return vm
            else:
                return None
        except Exception as e:
            print("VIF.get_vm Exception", e)
            return None

    def get_mac(self):
        try:
            mac = self.session.xenapi.VIF.get_MAC(self.vif)
            return mac
        except Exception as e:
            print("VIF.get_mac Exception", e)
            return None

    def get_mtu(self):
        try:
            return self.session.xenapi.VIF.get_MTU(self.vif)
        except Exception as e:
            print("VIF.get_mtu Exception", e)
            return None

    def get_qos_type(self):
        try:
            return self.session.xenapi.VIF.get_qos_algorithm_type(self.vif)
        except Exception as e:
            print("VIF.get_qos_type Exception", e)
            return None

    def set_qos_type(self, qos_type):
        try:
            return self.session.xenapi.VIF.get_qos_algorithm_type(self.vif, qos_type)
        except Exception as e:
            print("VIF.set_qos_type Exception", e)
            return False

    def get_qos_info(self):
        try:
            return self.session.xenapi.VIF.get_qos_algorithm_params(self.vif)
        except Exception as e:
            print("VIF.get_qos_info Exception", e)
            return None

    def set_qos_info(self, qos_params):
        try:
            self.session.xenapi.VIF.set_qos_algorithm_params(self.vif, qos_params)
            return True
        except Exception as e:
            print("VIF.set_qos_info Exception", e)
            return None

    def supported_qos_types(self):
        try:
            return self.session.xenapi.VIF.qos_supported_algorithms(self.vif)
        except Exception as e:
            print("VIF.supported_qos_types Exception", e)
            return None

    def get_address_v4(self):
        try:
            return self.session.xenapi.VIF.get_ipv4_addresses(self.vif)
        except Exception as e:
            print("VIF.get_address_v4 Exception", e)
            return None

    def get_gateway_v4(self):
        try:
            return self.session.xenapi.VIF.get_ipv4_gateway(self.vif)
        except Exception as e:
            print("VIF.get_gateway_v4 Exception", e)
            return None

    def get_address_v6(self):
        try:
            return self.session.xenapi.VIF.get_ipv6_addresses(self.vif)
        except Exception as e:
            print("VIF.get_address_v6 Exception", e)
            return None

    def get_gateway_v6(self):
        try:
            return self.session.xenapi.VIF.get_ipv6_gateway(self.vif)
        except Exception as e:
            print("VIF.get_gateway_v6 Exception", e)
            return None

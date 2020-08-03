from deprecated import deprecated


class Host:
    """ The Host Object """

    def __init__(self, session, host):
        self.session = session
        self.host = host

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns Host object that has specific uuid """
        try:
            host = session.xenapi.host.get_by_uuid(uuid)

            if host is not None:
                return Host(session, host)
            else:
                return None
        except Exception as e:
            print("Host.get_by_uuid Exception", e)
            return None

    @staticmethod
    def get_by_name(session, label):
        """ returns Host object that has specific name """
        try:
            host = session.xenapi.host.get_by_name_label(label)
            print(host)

            if host is not None:
                return Host(session, host)
            else:
                return None
        except Exception as e:
            print("Host.get_by_name Exception", e)
            return None

    @staticmethod
    def list_host(session):
        """gets Hosts available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of Host object)"""
        try:
            allHostList = []
            allHosts = session.xenapi.host.get_all()

            for hostF in allHosts:
                host = Host(session, hostF)
                allHostList.append(host)

            return allHostList
        except Exception as e:
            print("Host.list_host Exception", e)
            return None

    @deprecated
    def serialize(self) -> dict:

        return {
            "uuid": self.get_uuid(),
            "name": self.get_name(),
            "description": self.get_description(),
            "enabled": self.get_enabled(),
            "memory": {
                "free": self.get_free_memory(),
                "total": self.get_total_memory(),
            },
            "cpu": self.get_cpu_info(),
            "bios": self.get_bios_strings(),
            "version": self.get_software_version(),
        }

    def get_uuid(self):
        """ get UUID of Host """
        try:
            return self.session.xenapi.host.get_uuid(self.host)
        except Exception as e:
            print("Host.get_uuid Exception", e)
            return None

    def get_free_memory(self):
        """ get Free Memory of Host """
        try:
            return self.session.xenapi.host.compute_free_memory(self.host)
        except Exception as e:
            print("Host.get_free_memory Exception", e)
            return None

    def get_total_memory(self):
        """ get Total Memory of Host """
        try:
            metrics = self.session.xenapi.host.get_metrics(self.host)
            return self.session.xenapi.host_metrics.get_memory_total(metrics)
        except Exception as e:
            print("Host.get_memory_total Exception", e)
            return None

    def get_cpu_info(self):
        """ get CPU Info of Host """
        try:
            return self.session.xenapi.host.get_cpu_info(self.host)
        except Exception as e:
            print("Host.get_cpu_info Exception", e)
            return None

    def get_software_version(self):
        """ get Software Version of Host """
        try:
            return self.session.xenapi.host.get_software_version(self.host)
        except Exception as e:
            print("Host.get_software_version Exception", e)
            return None

    def disable(self):
        """ Disable Host """
        try:
            return self.session.xenapi.host.disable(self.host)
        except Exception as e:
            print("Host.disable Exception", e)
            return None

    def enable(self):
        """ Enable Host """
        try:
            return self.session.xenapi.host.enable(self.host)
        except Exception as e:
            print("Host.enable Exception", e)
            return None

    def get_enabled(self):
        """ Get Host is Enabled """
        try:
            return self.session.xenapi.host.get_enabled(self.host)
        except Exception as e:
            print("Host.get_enabled Exception", e)
            return None

    def evacuate(self):
        """ Evacuate Host """
        try:
            return self.session.xenapi.host.evacuate(self.host)
        except Exception as e:
            print("Host.evacuate Exception", e)
            return None

    def get_address(self):
        """ Get Address of Host """
        try:
            return self.session.xenapi.host.evacuate(self.host)
        except Exception as e:
            print("Host.get_address Exception", e)
            return None

    def get_bios_strings(self):
        """ Get BIOS Strings of Host """
        try:
            return self.session.xenapi.host.get_bios_strings(self.host)
        except Exception as e:
            print("Host.get_bios_strings Exception", e)
            return None

    def get_capabilities(self):
        """ Get capabilities of Host """
        try:
            return self.session.xenapi.host.get_capabilites(self.host)
        except Exception as e:
            print("Host.get_capabilities Exception", e)
            return None

    def get_name(self):
        """ Get name of Host """
        try:
            return self.session.xenapi.host.get_name_label(self.host)
        except Exception as e:
            print("Host.get_name Exception", e)
            return None

    def get_description(self):
        """ Get description of Host """
        try:
            return self.session.xenapi.host.get_description(self.host)
        except Exception as e:
            print("Host.get_description Exception", e)
            return None

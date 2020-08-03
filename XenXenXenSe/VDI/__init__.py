from deprecated import deprecated


class VDI:
    """ The Virtual Disk Image Object """

    def __init__(self, session, vdi):
        self.session = session
        self.vdi = vdi

    @staticmethod
    def get_by_name(session, name):
        """ returns SR object that has specific name """
        try:
            vdis = session.xenapi.VDI.get_by_name_label(name)

            vdi_list = []
            for vdi in vdis:
                vdi_list.append(VDI(session, vdi))

            return vdi_list
        except Exception as e:
            print("VDI.get_by_name Exception", e)
            return None

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns SR object that has specific uuid """
        try:
            vdi = session.xenapi.VDI.get_by_uuid(uuid)

            if vdi is not None:
                return VDI(session, vdi)
            else:
                return None
        except Exception as e:
            print("SR.get_by_uuid Exception", e)
            return None

    @staticmethod
    def get_all(session):
        """ returns SR object that exists on _host """
        try:
            vdis = session.xenapi.VDI.get_all()

            vdi_list = []
            for vdi in vdis:
                vdi_list.append(VDI(session, vdi))

            return vdi_list
        except Exception as e:
            print("VDI.get_all Exception", e)
            return None

    @deprecated
    def serialize(self) -> dict:
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "uuid": self.get_uuid(),
            "location": self.get_location(),
            "type": self.get_type(),
        }

    def get_name(self):
        try:
            return self.session.xenapi.VDI.get_name_label(self.vdi)
        except Exception as e:
            print("VDI.get_name Exception", e)
            return None

    def get_description(self):
        try:
            return self.session.xenapi.VDI.get_name_description(self.vdi)
        except Exception as e:
            print("VDI.get_description Exception", e)
            return None

    def get_uuid(self):
        try:
            return self.session.xenapi.VDI.get_uuid(self.vdi)
        except Exception as e:
            print("VDI.get_uuid Exception", e)
            return None

    def get_type(self):
        try:
            return self.session.xenapi.VDI.get_type(self.vdi)
        except Exception as e:
            print("VDI.get_type Exception", e)
            return None

    def get_location(self):
        try:
            return self.session.xenapi.VDI.get_location(self.vdi)
        except Exception as e:
            print("VDI.get_location Exception", e)
            return None

    def destroy(self):
        try:
            return self.session.xenapi.VDI.destroy(self.vdi)
        except Exception as e:
            print("VDI.get_location Exception", e)
            return None

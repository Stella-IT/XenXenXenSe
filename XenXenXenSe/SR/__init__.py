from deprecated import deprecated

from XenXenXenSe.VDI import VDI

class SR:
    """ The Storage Repository Object """

    def __init__(self, session, sr):
        self.session = session
        self.sr = sr

    @staticmethod
    def get_all(session):
        """ get all SR object available """
        try:
            srs = session.xenapi.SR.get_all()

            sr_list = []
            for sr in srs:
                sr_list.append(SR(session, sr))

            return sr_list
        except Exception as e:
            print("SR.get_by_uuid Exception", e)
            return None

    @staticmethod
    def get_by_name(session, name):
        """ returns SR object that has specific name"""
        try:
            srs = session.xenapi.SR.get_by_name_label(name)

            srs_list = []
            for sr in srs:
                srs_list.append(SR(session, sr))

            return srs_list
        except Exception as e:
            print("SR.get_by_name Exception", e)
            return None

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns SR object that has specific uuid """
        try:
            sr = session.xenapi.SR.get_by_uuid(uuid)

            if sr is not None:
                return SR(session, sr)
            else:
                return None
        except Exception as e:
            print("SR.get_by_uuid Exception", e)
            return None

    @deprecated
    def serialize(self) -> dict:
        """ Returns Info of this SR """
        vdis = self.get_VDIs()
        vdi_list = []

        if vdis is not None:
            for vdi in vdis:
                vdi_list.append(vdi.serialize())
        else:
            vdi_list = None

        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "size": self.get_physical_size(),
            "uuid": self.get_uuid(),
            "content_type": self.get_content_type(),
            "type": self.get_type(),
            "vdis": vdi_list
        }

    def get_VDIs(self):
        try:
            vdis = self.session.xenapi.SR.get_VDIs(self.sr)

            vdi_list = []
            for vdi in vdis:
                vdi_list.append(VDI(self.session, vdi))

            return vdi_list

        except Exception as e:
            print("SR.get_VDIs Exception", e)
            return

    def get_name(self):
        try:
            return self.session.xenapi.SR.get_name_label(self.sr)
        except Exception as e:
            print("SR.get_name Exception", e)
            return

    def get_description(self):
        try:
            return self.session.xenapi.SR.get_name_description(self.sr)
        except Exception as e:
            print("SR.get_description Exception", e)
            return None

    def get_physical_size(self):
        try:
            return self.session.xenapi.SR.get_physical_size(self.sr)
        except Exception as e:
            print("SR.get_physical_size Exception", e)
            return None

    def get_uuid(self):
        try:
            return self.session.xenapi.SR.get_uuid(self.sr)
        except Exception as e:
            print("SR.get_uuid Exception", e)
            return None

    def get_content_type(self):
        try:
            return self.session.xenapi.SR.get_content_type(self.sr)
        except Exception as e:
            print("SR.get_content_type Exception", e)
            return None

    def get_type(self):
        try:
            return self.session.xenapi.SR.get_type(self.sr)
        except Exception as e:
            print("SR.get_type Exception", e)
            return None

    def scan(self):
        try:
            self.session.xenapi.SR.scan(self.sr)
        except Exception as e:
            print("SR.scan Exception", e)
            return False

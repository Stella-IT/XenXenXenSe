from deprecated import deprecated


class GuestMetrics:
    def __init__(self, session, guest):
        self.session = session
        self.guest = guest

    @deprecated
    def serialize(self):
        return {
            "uuid": self.get_uuid(),
            "os": self.get_os_version(),
            "networks": self.get_networks(),
        }

    def get_uuid(self):
        """ Gets UUID of Guest Metrics """
        try:
            return self.session.xenapi.VM_guest_metrics.get_uuid(self.guest)
        except Exception as e:
            print("Exception: GuestMetrics.get_uuid:", e)
            return None

    def get_networks(self):
        """ Gets UUID of Guest Networks """
        try:
            return self.session.xenapi.VM_guest_metrics.get_networks(
                self.guest
            )
        except Exception as e:
            print("Exception: GuestMetrics.get_networks:", e)
            return None

    def get_os_version(self):
        """ Gets OS Version of Guest """
        try:
            return self.session.xenapi.VM_guest_metrics.get_os_version(
                self.guest
            )
        except Exception as e:
            print("Exception: GuestMetrics.get_os_version:", e)
            return None

    def get_other(self):
        """ Gets "Other" of Guest """
        try:
            return self.session.xenapi.VM_guest_metrics.get_other(self.guest)
        except Exception as e:
            print("Exception: GuestMetrics.get_others:", e)
            return None

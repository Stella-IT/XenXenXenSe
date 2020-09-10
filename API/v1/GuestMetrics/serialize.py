from XenGarden.GuestMetrics import GuestMetrics


def serialize(guest: GuestMetrics):
    return dict(
        uuid=guest.get_uuid(),
        os=guest.get_os_version(),
        networks=guest.get_networks()
    )

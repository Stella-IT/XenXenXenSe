from XenGarden.VDI import VDI


def serialize(vdi: VDI):
    return dict(
        name=vdi.get_name(),
        description=vdi.get_description(),
        uuid=vdi.get_uuid(),
        location=vdi.get_location(),
        type=vdi.get_type()
    )

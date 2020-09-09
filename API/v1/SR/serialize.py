from XenGarden.SR import SR

from ..VDI.serialize import serialize as _vdi_serialize


def serialize(sr: SR):
    vdis = sr.get_VDIs()
    vdi_list = []

    if vdis is not None:
        for vdi in vdis:
            vdi_list.append(_vdi_serialize(vdi))
    else:
        vdi_list = None

    return {
        "name": sr.get_name(),
        "description": sr.get_description(),
        "size": sr.get_physical_size(),
        "uuid": sr.get_uuid(),
        "content_type": sr.get_content_type(),
        "type": sr.get_type(),
        "vdis": vdi_list,
    }

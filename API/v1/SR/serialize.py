import asyncio

from XenGarden.SR import SR

from API.v1.VDI.serialize import serialize as _vdi_serialize


async def serialize(sr: SR):
    vdis = sr.get_VDIs()
    __vdi_list = []
    if vdis is not None:
        __vdi_list = await asyncio.gather(*[_vdi_serialize(vdi) for vdi in vdis])
    else:
        __vdi_list = None

    return dict(
        name=sr.get_name(),
        description=sr.get_description(),
        size=sr.get_physical_size(),
        used=sr.get_physical_utilisation(),
        free=sr.get_physical_size() - sr.get_physical_utilisation(),
        uuid=sr.get_uuid(),
        content_type=sr.get_content_type(),
        type=sr.get_type(),
        vdis=__vdi_list,
    )

from fastapi import APIRouter

from XenGarden.VDI import VDI
from XenGarden.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/vdi/list")
async def vdi_list(cluster_id: str):
    """ Get VDI by UUID """
    session = create_session(cluster_id)
    vdis = VDI.get_all(session)

    vdi_list = []
    for vdi in vdis:
        vdi_list.append(serialize(vdi))

    if vdis is not None:
        ret = {"success": True, "data": vdi_list}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

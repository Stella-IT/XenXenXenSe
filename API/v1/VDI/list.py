from fastapi import APIRouter

from XenXenXenSe.VDI import VDI
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vdi/list")
async def vdi_list(cluster_id: str):
    """ Get VDI by UUID """
    session = create_session(cluster_id)
    vdis = VDI.get_all(session)

    vdi_list = []
    for vdi in vdis:
        vdi_list.append(vdi.serialize())

    if vdis is not None:
        ret = {"success": True, "data": vdi_list}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter

from XenXenXenSe.VDI import VDI
from XenXenXenSe.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/vdi/{vdi_uuid}")
async def vdi_get_by_uuid(cluster_id: str, vdi_uuid: str):
    """ Get VDI by UUID """
    session = create_session(cluster_id)
    vdi: VDI = VDI.get_by_uuid(session, vdi_uuid)

    if vdi is not None:
        ret = {"success": True, "data": serialize(vdi)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

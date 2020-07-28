from fastapi import APIRouter

from XenXenXenSe.VBD import VBD
from XenXenXenSe.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/vbd/{vbd_uuid}")
async def vbd_get_by_uuid(cluster_id: str, vbd_uuid: str):
    """ Get VBD by UUID """
    session = create_session(cluster_id)
    vbd: VBD = VBD.get_by_uuid(session, vbd_uuid)

    if vbd is not None:
        ret = {"success": True, "data": serialize(vbd)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

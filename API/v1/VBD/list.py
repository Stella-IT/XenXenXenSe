from fastapi import APIRouter

from XenXenXenSe.VBD import VBD
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vbd/list")
async def vbd_list(cluster_id: str):
    """ Get VBD by UUID """
    session = create_session(cluster_id)
    vbds = VBD.get_all(session)

    vbd_list = []
    for vbd in vbds:
        vbd_list.append(vbd.serialize())

    if vbds is not None:
        ret = {"success": True, "data": vbd_list}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter

from XenGarden.VBD import VBD
from XenGarden.session import create_session

router = APIRouter()


@router.delete("/{cluster_id}/vbd/{vbd_uuid}")
@router.get("/{cluster_id}/vbd/{vbd_uuid}/delete")
async def vbd_delete(cluster_id: str, vbd_uuid: str):
    """ Destroy VBD by UUID """
    session = create_session(cluster_id)
    vbd: VBD = VBD.get_by_uuid(session, vbd_uuid)

    if vbd is not None:
        ret = {"success": True, "data": vbd.destroy()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

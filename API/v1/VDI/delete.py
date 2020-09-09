from fastapi import APIRouter

from XenGarden.VDI import VDI
from XenGarden.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vdi/{vdi_uuid}/delete")
@router.delete("/{cluster_id}/vdi/{vdi_uuid}")
async def vdi_get_by_uuid(cluster_id: str, vdi_uuid: str):
    """ Delete SR by UUID """
    session = create_session(cluster_id)
    vdi: VDI = VDI.get_by_uuid(session, vdi_uuid)

    if vdi is not None:
        ret = {"success": vdi.destroy()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

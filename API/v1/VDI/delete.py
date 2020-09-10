from fastapi import APIRouter

from XenGarden.VDI import VDI
from XenGarden.session import create_session
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vdi/{vdi_uuid}/delete")
@router.delete("/{cluster_id}/vdi/{vdi_uuid}")
async def vdi_get_by_uuid(cluster_id: str, vdi_uuid: str):
    """ Delete SR by UUID """
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())
    vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)

    if vdi is not None:
        ret = dict(success=vdi.destroy())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret
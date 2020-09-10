from fastapi import APIRouter

from XenGarden.VDI import VDI
from XenGarden.session import create_session

from API.v1.VDI.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vdi/{vdi_uuid}")
async def vdi_get_by_uuid(cluster_id: str, vdi_uuid: str):
    """ Get VDI by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)

    if vdi is not None:
        ret = dict(success=True, data=serialize(vdi))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VBD import VBD

from API.v1.VBD.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vbd/{vbd_uuid}")
async def vbd_get_by_uuid(cluster_id: str, vbd_uuid: str):
    """ Get VBD by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

    if vbd is not None:
        ret = dict(success=True, data=serialize(vbd))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

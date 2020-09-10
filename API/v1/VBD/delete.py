from fastapi import APIRouter

from XenGarden.VBD import VBD
from XenGarden.session import create_session
from config import get_xen_clusters

router = APIRouter()


@router.delete("/{cluster_id}/vbd/{vbd_uuid}")
@router.get("/{cluster_id}/vbd/{vbd_uuid}/delete")
async def vbd_delete(cluster_id: str, vbd_uuid: str):
    """ Destroy VBD by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

    if vbd is not None:
        ret = dict(success=True, data=vbd.destroy())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

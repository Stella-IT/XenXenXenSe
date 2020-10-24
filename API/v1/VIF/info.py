from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.VIF.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}")
async def vif_get_by_uuid(cluster_id: str, vif_uuid: str):
    """ Get VIF by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

    if vif is not None:
        ret = dict(success=True, data=serialize(vif))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

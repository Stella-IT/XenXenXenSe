from fastapi import APIRouter
from XenGarden.GuestMetrics import GuestMetrics
from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.GuestMetrics.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/guest/{guest_uuid}")
async def guest_get_by_uuid(cluster_id: str, guest_uuid: str):
    """ Get GuestMetrics by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    guest: GuestMetrics = Host.get_by_uuid(session=session, uuid=guest_uuid)

    if guest is not None:
        ret = dict(success=True, data=serialize(guest))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

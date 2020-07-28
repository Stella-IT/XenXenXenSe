from fastapi import APIRouter

from XenXenXenSe.GuestMetrics import GuestMetrics
from XenXenXenSe.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/guest/{guest_uuid}")
async def guest_get_by_uuid(cluster_id: str, guest_uuid: str):
    """ Get GuestMetrics by UUID """
    session = create_session(cluster_id)
    guest: GuestMetrics = Host.get_by_uuid(session, guest_uuid)

    if host is not None:
        ret = {"success": True, "data": serialize(guest)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

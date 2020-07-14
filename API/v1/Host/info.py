from fastapi import APIRouter

from XenXenXenSe.Host import Host
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/host/{host_uuid}")
async def host_get_by_uuid(cluster_id: str, host_uuid: str):
    """ Get Host by UUID """
    session = create_session(cluster_id)
    host: Host = Host.get_by_uuid(session, host_uuid)

    if host is not None:
        ret = {"success": True, "data": host.serialize()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter
from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.Host.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/host/{host_uuid}")
async def host_get_by_uuid(cluster_id: str, host_uuid: str):
    """ Get Host by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    host: Host = Host.get_by_uuid(session=session, uuid=host_uuid)

    if host is not None:
        ret = dict(success=True, data=serialize(host))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter

from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.Host.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/host/list")
async def host_list(cluster_id: str):
    """ Get All from Existance Host """
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())
    hosts = Host.list_host(session=session)

    __hosts_list = []
    hosts_list = __hosts_list.append

    for host in hosts:
        hosts_list(serialize(host))

    ret = dict(
        success=True,
        data=__hosts_list
    )

    session.xenapi.session.logout()
    return ret

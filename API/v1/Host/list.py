from fastapi import APIRouter

from XenXenXenSe.Host import Host
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/host/list")
async def host_list(cluster_id: str):
    """ Get All from Existance Host """
    session = create_session(cluster_id)
    hosts = Host.list_host(session)

    hosts_list = []
    for host in hosts:
        hosts_list.append(host.serialize())

    ret = {
        "success": True,
        "data": hosts_list
    }

    session.xenapi.session.logout()
    return ret

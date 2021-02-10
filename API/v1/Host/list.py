from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException, Path
from XenAPI.XenAPI import Failure
from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Host.serialize import serialize
from app.settings import Settings
import asyncio

router = APIRouter()


@router.get("/{cluster_id}/host/list")
async def host_list(
    cluster_id: str = Path(default=None, title="cluster_id", description="Cluster ID")
):
    """ Get All from Existance Host """
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        hosts = Host.list_host(session=session)

        __hosts_list = await asyncio.gather(*[serialize(host) for host in hosts])
        
        ret = dict(success=True, data=__hosts_list)

        session.xenapi.session.logout()
        return ret
    except Failure as xenapi_error:
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

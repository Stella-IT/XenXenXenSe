from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException, Path
from XenAPI.XenAPI import Failure
from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Host.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/host/{host_uuid}")
async def host_get_by_uuid(
    cluster_id: str = Path(default=None, title="cluster_id", description="Cluster ID"),
    host_uuid: str = Path(default=None, title="host_uuid", description="Host UUID"),
):
    """ Get Host by UUID """
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        host: Host = Host.get_by_uuid(session=session, uuid=host_uuid)

        if host is not None:
            ret = dict(success=True, data=await serialize(host))
        else:
            ret = dict(success=False)

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

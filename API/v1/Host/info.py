from fastapi import APIRouter, HTTPException, Path
from xmlrpc.client import Fault
from http.client import RemoteDisconnected

from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.Host.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/host/{host_uuid}")
async def host_get_by_uuid(
        cluster_id: str = Path(default=None, title="cluster_id", description="Cluster ID"),
        host_uuid: str = Path(default=None, title="host_uuid", description="Host UUID"),
    ):
    """ Get Host by UUID """
    try:
        # KeyError Handling
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(status_code=400, detail=f"{key_error} is not a valid path")

        host: Host = Host.get_by_uuid(session=session, uuid=host_uuid)

        if host is not None:
            ret = dict(success=True, data=serialize(host))
        else:
            ret = dict(success=False)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(status_code=int(xml_rpc_error.faultCode), detail=xml_rpc_error.faultString)
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
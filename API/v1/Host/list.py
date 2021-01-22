from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.Host.serialize import serialize
from API.v1.model.host import HLResponseModel
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/host/list", response_model=HLResponseModel)
async def host_list(
    cluster_id: str = Path(default=None, title="cluster_id", description="Cluster ID")
):
    """ Get All from Existance Host """
    try:
        # KeyError Handling
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        hosts = Host.list_host(session=session)

        __hosts_list = []
        hosts_list = __hosts_list.append

        for host in hosts:
            hosts_list(serialize(host))

        ret = dict(success=True, data=__hosts_list)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

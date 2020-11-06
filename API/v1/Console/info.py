from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException, Path
from XenGarden.Console import Console
from XenGarden.session import create_session

from API.v1.Console.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/console/{console_uuid}")
async def console_get_by_uuid(
    cluster_id: str = Path(
        default=None, title="cluster_id", description="Cluster ID"
    ),
    console_uuid: str = Path(
        default=None, title="console_uuid", description="Console UUID"
    ),
):
    """ Get Console by UUID """
    try:
        # KeyError Handling
        try:
            session = create_session(
                cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        console: Console = Console.get_by_uuid(session, console_uuid)

        if console is not None:
            ret = dict(success=True, data=serialize(console))
        else:
            ret = dict(success=False)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

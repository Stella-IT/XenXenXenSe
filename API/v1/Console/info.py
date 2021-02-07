from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.Console import Console
from XenGarden.session import create_session

from API.v1.Console.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/console/{console_uuid}")
async def console_get_by_uuid(
    cluster_id: str,
    console_uuid: str,
):
    """ Get Console by UUID """
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session, "")
        console: Console = Console.get_by_uuid(session, console_uuid)
        print(console.get_protocol())

        if console is not None:
            ret = dict(success=True, data=serialize(console))
        else:
            ret = dict(success=False)

        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

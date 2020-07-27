from fastapi import APIRouter

from XenXenXenSe.Console import Console
from XenXenXenSe.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/console/{console_uuid}")
async def console_get_by_uuid(cluster_id: str, console_uuid: str):
    """ Get Console by UUID """
    session = create_session(cluster_id)
    console: Console = Console.get_by_uuid(session, console_uuid)

    if host is not None:
        ret = {"success": True, "data": serialize(console)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

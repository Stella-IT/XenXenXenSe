from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter
from fastapi import HTTPException
from XenGarden.session import create_session
from XenGarden.VBD import VBD

from API.v1.VBD.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vbd/{vbd_uuid}")
async def vbd_get_by_uuid(cluster_id: str, vbd_uuid: str):
    """ Get VBD by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

        if vbd is not None:
            ret = dict(success=True, data=serialize(vbd))
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

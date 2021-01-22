from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VDI import VDI

from API.v1.model.vdi import VDInfoResponseModel
from API.v1.VDI.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vdi/{vdi_uuid}", response_model=VDInfoResponseModel)
async def vdi_get_by_uuid(cluster_id: str, vdi_uuid: str):
    """ Get VDI by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)

        if vdi is not None:
            ret = dict(success=True, data=serialize(vdi))
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

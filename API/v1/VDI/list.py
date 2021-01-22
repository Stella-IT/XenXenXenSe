from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter
from fastapi import HTTPException
from XenGarden.session import create_session
from XenGarden.VDI import VDI

from API.v1.model.vdi import VDLResponseModel
from API.v1.VDI.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vdi/list", response_model=VDLResponseModel)
async def vdi_list(cluster_id: str):
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

        vdis = VDI.get_all(session=session)

        __vdi_list = []
        _vdi_list = __vdi_list.append
        for vdi in vdis:
            _vdi_list(serialize(vdi))

        if vdis is not None:
            ret = dict(success=True, data=__vdi_list)
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

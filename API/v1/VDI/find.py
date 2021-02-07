from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VDI import VDI

from API.v1.Interface import NameArgs
from API.v1.model.VDI import VDIFindResponseModel
from API.v1.VDI.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vdi/find", response_model=VDIFindResponseModel)
async def find_VDI_by_name(cluster_id: str, args: NameArgs):
    """ Find VDI by Name """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        name = args.name
        vdis = VDI.get_by_name(session=session, name=name)

        if vdis is not None:
            __vdis_list = []
            for vdi in vdis:
                __vdis_list.append(serialize(vdi))

            ret = dict(success=True, data=__vdis_list)
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

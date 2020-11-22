from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VDI import VDI

from API.v1.Interface import NameArgs
from API.v1.model.vdi import VDIFindResponseModel
from API.v1.VDI.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vdi/find", response_model=VDIFindResponseModel)
async def find_VDI_by_name(cluster_id: str, args: NameArgs):
    """ Find VDI by Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        name = args.name
        vdis = VDI.get_by_name(session=session, name=name)

        if vdis is not None:
            __vdis_list = []
            vdis_list = __vdis_list.append
            for vdi in vdis:
                vdis_list(serialize(vdi))

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


@router.get("/{cluster_id}/vdi/find/{iso_name}", response_model=VDIFindResponseModel)
async def insert_cd_inurl_name(cluster_id: str, iso_name: str):
    """ Find VDI by Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vdis = VDI.get_by_name(session=session, name=iso_name)
        print(vdis)

        if vdis is not None:
            __vdis_list = []
            vdis_list = __vdis_list.append
            for vdi in vdis:
                vdis_list(serialize(vdi))

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

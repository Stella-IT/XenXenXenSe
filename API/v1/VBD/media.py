from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VBD import VBD
from XenGarden.VDI import VDI

from API.v1.Interface import UUIDArgs
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vbd/{vbd_uuid}/insert/{vdi_uuid}")
async def vbd_insert_vdi_by_uuid(
    cluster_id: str, vbd_uuid: str, vdi_uuid: str
):
    """ Insert VDI into VBD by UUID """
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

        if vdi is None:
            ret = dict(success=False)
            session.xenapi.session.logout()
            return ret

        vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

        if vbd is not None:
            ret = dict(success=vbd.insert(vdi))
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


@router.put("/{cluster_id}/vbd/{vbd_uuid}/insert")
async def vbd_insert_vdi_by_uuid(
    cluster_id: str, vbd_uuid: str, res: UUIDArgs
):
    """ Insert VDI into VBD by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vdi: VDI = VDI.get_by_uuid(session=session, uuid=res.uuid)

        if vdi is None:
            ret = dict(success=False)
            session.xenapi.session.logout()
            return ret

        vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

        if vbd is not None:
            ret = dict(success=vbd.insert(vdi))
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


@router.delete("/{cluster_id}/vbd/{vbd_uuid}/insert")
@router.get("/{cluster_id}/vbd/{vbd_uuid}/eject")
async def vbd_eject_vdi(cluster_id: str, vbd_uuid: str):
    """ Eject VDI from VBD """
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
            ret = dict(success=vbd.eject())
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

from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

from .model import ModeModel

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}/lock")
async def vif_get_lock_by_uuid(cluster_id: str, vif_uuid: str):
    """ Get VIF Lock by UUID """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)
        ret = dict(success=True, data={"mode": vif.get_locking_mode()})

        session.xenapi.session.logout()
        return ret
    except Failure as xenapi_error:
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)


@router.put("/{cluster_id}/vif/{vif_uuid}/lock")
async def vif_set_lock_by_uuid(cluster_id: str, vif_uuid: str, data: ModeModel):
    """ Set VIF Lock Data by UUID """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)
        vif.set_locking_mode(data.mode)

        ret = dict(success=True)

        session.xenapi.session.logout()
        return ret
    except Failure as xenapi_error:
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)


@router.delete("/{cluster_id}/vif/{vif_uuid}/lock")
async def vif_clear_lock_by_uuid(cluster_id: str, vif_uuid: str, data: ModeModel):
    """ Clear VIF Lock Data to Default by UUID """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)
        vif.set_locking_mode("network_default")

        ret = dict(success=True)

        session.xenapi.session.logout()
        return ret
    except Failure as xenapi_error:
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VBD import VBD

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vbd/{vbd_uuid}/plug")
@router.post("/{cluster_id}/vbd/{vbd_uuid}/plug")
async def _vbd_plug(cluster_id: str, vbd_uuid: str):
    """Plug into VBD"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

        if vbd is not None:
            ret = dict(success=vbd.plug())
        else:
            ret = dict(success=False)

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


@router.delete("/{cluster_id}/vbd/{vbd_uuid}/plug")
@router.get("/{cluster_id}/vbd/{vbd_uuid}/unplug")
@router.post("/{cluster_id}/vbd/{vbd_uuid}/unplug")
async def vbd_unplug(cluster_id: str, vbd_uuid: str):
    """Unplug from VBD"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )
        vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

        if vbd is not None:
            ret = dict(success=vbd.unplug())
        else:
            ret = dict(success=False)

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

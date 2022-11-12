from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VDI import VDI

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vdi/{vdi_uuid}/sr{url_after:path}")
@router.post("/{cluster_id}/vdi/{vdi_uuid}/sr{url_after:path}")
@router.patch("/{cluster_id}/vdi/{vdi_uuid}/sr{url_after:path}")
@router.put("/{cluster_id}/vdi/{vdi_uuid}/sr{url_after:path}")
@router.delete("/{cluster_id}/vdi/{vdi_uuid}/sr{url_after:path}")
async def vdi_get_sr(cluster_id: str, vdi_uuid: str, url_after: str = ""):
    """Redirect To SR"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)
        sr = None

        try:
            sr = vdi.get_SR()
        except Exception:
            session.xenapi.session.logout()
            raise HTTPException(
                status_code=404, detail=f"VDI {vdi_uuid} does not have proper SR"
            )

        sr_uuid = sr.get_uuid()

        session.xenapi.session.logout()
        return RedirectResponse(f"/v1/{cluster_id}/sr/{sr_uuid}{url_after}")
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

from typing import Optional
from xmlrpc.client import Fault

from fastapi import APIRouter, Depends, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VBD import VBD

from API.v1.Common import xenapi_failure_jsonify
from API.v1.VBD.delete import router as _vbd_delete
from API.v1.VBD.find_vdi import router as _vbd_find_by_vdi
from API.v1.VBD.info import router as _vbd_info
from API.v1.VBD.list import router as _vbd_list
from API.v1.VBD.media import router as _vbd_media
from app.settings import Settings


# === Condition Checker ===
async def verify_vbd_uuid(cluster_id: str, vbd_uuid: Optional[str] = None):
    if vbd_uuid is None:
        return

    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        vbd = VBD.get_by_uuid(session, vbd_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(
                status_code=404, detail=f"VBD {vbd_uuid} does not exist"
            )

        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )

    session.xenapi.session.logout()


# === Router Actions ===
vbd_router = APIRouter(dependencies=[Depends(verify_vbd_uuid)])

vbd_router.include_router(_vbd_list, tags=["vbd"])
vbd_router.include_router(_vbd_info, tags=["vbd"])
vbd_router.include_router(_vbd_find_by_vdi, tags=["vbd"])
vbd_router.include_router(_vbd_media, tags=["vbd"])
vbd_router.include_router(_vbd_delete, tags=["vbd"])

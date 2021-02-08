from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from XenGarden.session import create_session
from XenGarden.VM import VM

from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/cd{url_after:path}")
@router.post("/{cluster_id}/vm/{vm_uuid}/cd{url_after:path}")
@router.patch("/{cluster_id}/vm/{vm_uuid}/cd{url_after:path}")
@router.put("/{cluster_id}/vm/{vm_uuid}/cd{url_after:path}")
@router.delete("/{cluster_id}/vm/{vm_uuid}/cd{url_after:path}")
async def get_cd(cluster_id: str, vm_uuid: str, url_after: str = ""):
    from XenGarden.VBD import VBD

    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        vbd: VBD = vm.get_CD()
        vbd_uuid = vbd.get_uuid()

        session.xenapi.session.logout()

        return RedirectResponse(url=f"/v1/{cluster_id}/vbd/{vbd_uuid}{url_after}")
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

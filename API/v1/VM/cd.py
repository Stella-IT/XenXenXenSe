from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException, Request
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.VBD.serialize import serialize as _vbd_serialize
from app.settings import Settings
from starlette.responses import RedirectResponse

router = APIRouter()


@router.route("/{cluster_id}/vm/{vm_uuid}/cd{url_after:path}")
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

        return RedirectResponse(url=f'/{cluster_id}/vbd/{vbd_uuid}{url_after}')
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)


@router.get("/{cluster_id}/vm/{vm_uuid}/cds")
async def get_cds(cluster_id: str, vm_uuid: str):
    from XenGarden.VBD import VBD

    try:
        session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        if vm is not None:

            new_vbds = vm.get_CDs()

            __vbd_serialized = []
            if new_vbds is not None:
                for vbd in new_vbds:
                    if vbd is not None:
                        __vbd_serialized.append(_vbd_serialize(vbd))

                ret = dict(success=True, data=__vbd_serialized)
            else:
                ret = dict(success=False)
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

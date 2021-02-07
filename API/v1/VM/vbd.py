from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.VBD.serialize import serialize as _vbd_serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vbds")
async def instance_vbds(cluster_id: str, vm_uuid: str):
    """ Show Instance VBDs """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        if vm is not None:

            newVBDs = vm.get_VBDs()

            __vbd_serialized = []

            if newVBDs is not None:
                for vbd in newVBDs:
                    if vbd is not None:
                        __vbd_serialized.append(_vbd_serialize(vbd))

                print(__vbd_serialized)

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

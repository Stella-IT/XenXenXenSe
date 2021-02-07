from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.VIF.serialize import serialize as _vif_serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vifs")
async def instance_vifs(cluster_id: str, vm_uuid: str):
    """ Show Instnace VIFs """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        if vm is not None:

            new_vifs = vm.get_VIFs()

            __vif_serialized = []

            if new_vifs is not None:
                for vif in new_vifs:
                    if vif is not None:
                        __vif_serialized.append(_vif_serialize(vif))

                ret = dict(success=True, data=__vif_serialized)
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

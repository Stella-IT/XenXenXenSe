from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VBD import VBD

from API.v1.Common import xenapi_failure_jsonify
from API.v1.VBD.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vbd/find-by-vdi/{vdi_uuid}")
async def vbd_list(cluster_id: str, vdi_uuid: str):
    """Get VBD by UUID"""

    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vbds = VBD.get_all(session=session)

        __vbd_list = []
        for vbd in vbds:
            if vbd.get_VDI().get_uuid() == vdi_uuid:
                __vbd_list.append(await serialize(vbd))

        if vbds is not None:
            ret = dict(success=True, data=__vbd_list)
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

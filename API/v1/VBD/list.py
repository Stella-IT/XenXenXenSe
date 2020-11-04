from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VBD import VBD

from API.v1.VBD.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vbd/list")
async def vbd_list(cluster_id: str):
    """ Get VBD by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vbds = VBD.get_all(session)

        __vbd_list = []
        _vbd_list = __vbd_list.append
        for vbd in vbds:
            _vbd_list(serialize(vbd))

        if vbds is not None:
            ret = dict(success=True, data=__vbd_list)
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

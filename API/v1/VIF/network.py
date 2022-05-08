from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from starlette.responses import RedirectResponse
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.Common import xenapi_failure_jsonify
from API.v1.VIF.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}/network{url_after:path}")
@router.post("/{cluster_id}/vif/{vif_uuid}/network{url_after:path}")
@router.patch("/{cluster_id}/vif/{vif_uuid}/network{url_after:path}")
@router.put("/{cluster_id}/vif/{vif_uuid}/network{url_after:path}")
@router.delete("/{cluster_id}/vif/{vif_uuid}/network{url_after:path}")
async def vif_get_network(cluster_id: str, vif_uuid: str, url_after: str = ""):
    """Redirect To VIF's Network"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

        if vif is None:
            session.xenapi.session.logout()
            raise HTTPException(
                status_code=404, detail=f"VIF {vif_uuid} does not exist"
            )

        network = vif.get_network()

        if network is None: 
            session.xenapi.session.logout()
            raise HTTPException(
                status_code=404, detail=f"VIF {vif_uuid} does not exist on ANY Network"
            )
        
        network_uuid = network.get_uuid()

        session.xenapi.session.logout()
        return RedirectResponse(f"/v1/{cluster_id}/network/{network_uuid}{url_after}")
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

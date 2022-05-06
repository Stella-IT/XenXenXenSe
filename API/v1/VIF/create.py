from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.Common import xenapi_failure_jsonify
from API.v1.VIF.model import VIFCreateModel
from API.v1.VIF.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vif")
async def vif_create(cluster_id: str, vif_model: VIFCreateModel):
    """Create VIF with provided parameters"""
    try:
        params = vif_model.dict()
        if params.get("other_config") is None:
            params["other_config"] = dict()

        if params.get("qos_algorithm_type") is None:
            params["qos_algorithm_type"] = ""
            params["qos_algorithm_params"] = dict()

        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.create(session, params)

        if vif is not None:
            ret = dict(success=True, data=await serialize(vif))
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

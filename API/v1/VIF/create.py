from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.Network import Network
from XenGarden.session import create_session
from XenGarden.VIF import VIF
from XenGarden.VM import VM

from API.v1.Common import xenapi_failure_jsonify
from API.v1.VIF.model import VIFCreateModel
from API.v1.VIF.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vif")
async def vif_create(cluster_id: str, vif_model: VIFCreateModel):
    """Create VIF with provided parameters"""
    try:
        params = vif_model.dict(exclude_unset=True)
        if params.get("other_config") is None:
            params["other_config"] = dict()

        if params.get("qos_algorithm_type") is None:
            params["qos_algorithm_type"] = ""
            params["qos_algorithm_params"] = dict()

        mtu = params.get("mtu")
        if mtu is None:
            params["mtu"] = 1500

        mac = params.get("mac")
        if mac is None:
            import random

            sample_mac = "52:54:00:%02x:%02x:%02x" % (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

            params["mac"] = sample_mac

        if params.get("vm") is None or params.get("network") is None:
            raise HTTPException(
                status_code=400,
                detail=dict(type="invalid_request", error="missing required parameter"),
            )

        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm = VM.get_by_uuid(session, params.get("vm"))
        network = Network.get_by_uuid(session, params.get("network"))

        if vm is None or network is None:
            raise HTTPException(
                status_code=404,
                detail=dict(
                    type="not_found", error="requested resource could not be found"
                ),
            )

        params["network"] = network
        params["vm"] = vm

        vif: VIF = VIF.create(session, **params)

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

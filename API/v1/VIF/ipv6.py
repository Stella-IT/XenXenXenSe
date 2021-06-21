from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

from .model import IPModel

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}/ipv6")
async def vif_get_ipv6_by_uuid(cluster_id: str, vif_uuid: str):
    """Get VIF IPv6 by UUID"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)
        ret = dict(
            success=True,
            data=dict(
                address=vif.get_address_v6(),
                gateway=vif.get_gateway_v6(),
            ),
        )

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


@router.put("/{cluster_id}/vif/{vif_uuid}/ipv6")
async def vif_set_ipv6_by_uuid(cluster_id: str, vif_uuid: str, data: IPModel):
    """Set VIF IPv6 Data by UUID"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)
        result = vif.config_ipv6(
            "Static", data.address, "" if data.gateway is None else data.gateway
        )

        ret = dict(success=True, data=result)

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

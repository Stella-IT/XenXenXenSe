from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Interface import QoSTypeArgs
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}/qos")
async def vif_get_qos_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS by UUID """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

        if vif is not None:
            ret = dict(
                success=True,
                data=dict(type=vif.get_qos_type(), info=vif.get_qos_info()),
            )
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


@router.put("/{cluster_id}/vif/{vif_uuid}/qos")
async def vif_get_qos_type_by_uuid(cluster_id: str, vif_uuid: str, data: QoSTypeArgs):
    """ Set VIF QoS Data by UUID """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

        result = True
        if data.type is not None:
            vif.set_qos_type(data.type)

        if data.info is not None:
            vif.set_qos_info(data.info)

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

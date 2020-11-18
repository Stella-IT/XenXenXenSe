from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}/qos")
async def vif_get_qos_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
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
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)


@router.get("/{cluster_id}/vif/{vif_uuid}/qos/type")
async def vif_get_qos_type_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS Type by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

        if vif is not None:
            ret = dict(success=True, data=vif.get_qos_type())
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


@router.get("/{cluster_id}/vif/{vif_uuid}/qos/speed")
async def vif_get_qos_speed_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS Type by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )
        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

        if vif is not None:
            ret = dict(success=True, data=vif.get_qos_info()["kbps"])
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


@router.get("/{cluster_id}/vif/{vif_uuid}/qos/speed/{speed}")
async def vif_set_qos_speed_by_uuid(cluster_id: str, vif_uuid: str, speed: str):
    """ Set VIF QoS Speed by UUID """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

        speedNum = speed

        try:
            speedNum = int(speed)
        except ValueError:
            return dict(success=False)

        if speedNum <= 0:
            a = vif.set_qos_type("")
            b = vif.set_qos_info({})

            ret = dict(success=a and b)

        else:
            if vif is not None:
                if vif.get_qos_type() != "ratelimit":
                    vif.set_qos_type("ratelimit")

                ret = dict(success=vif.set_qos_info(dict(kbps=speed)))
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

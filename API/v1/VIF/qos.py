from fastapi import APIRouter

from XenXenXenSe.VIF import VIF
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}/qos")
async def vif_get_qos_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS by UUID """
    session = create_session(cluster_id)
    vif: VIF = VIF.get_by_uuid(session, vif_uuid)

    if vif is not None:
        ret = {"success": True, "data": {
          "type": vif.get_qos_type(),
          "info": vif.get_qos_info()
        }}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vif/{vif_uuid}/qos/type")
async def vif_get_qos_type_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS Type by UUID """
    session = create_session(cluster_id)
    vif: VIF = VIF.get_by_uuid(session, vif_uuid)

    if vif is not None:
        ret = {"success": True, "data": vif.get_qos_type()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/vif/{vif_uuid}/qos/speed")
async def vif_get_qos_speed_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS Type by UUID """
    session = create_session(cluster_id)
    vif: VIF = VIF.get_by_uuid(session, vif_uuid)

    if vif is not None:
        ret = {"success": True, "data": vif.get_qos_info()['kbps']}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/vif/{vif_uuid}/qos/speed/{speed}")
async def vif_set_qos_speed_by_uuid(cluster_id: str, vif_uuid: str, speed: str):
    """ Set VIF QoS Speed by UUID """
    session = create_session(cluster_id)
    vif: VIF = VIF.get_by_uuid(session, vif_uuid)

    speedNum = speed

    try:
        speedNum = int(speed)
    except ValueError:
        return {"success": False}

    if speedNum <= 0:
        a = vif.set_qos_type("")
        b = vif.set_qos_info({})

        ret = {"success": a and b}
        
    else:
        if vif is not None:        
            if vif.get_qos_type() != "ratelimit":
                vif.set_qos_type("ratelimit")

            ret = {"success": vif.set_qos_info({
                "kbps": speed
            })}
        else:
            ret = {"success": False}

    session.xenapi.session.logout()
    return ret

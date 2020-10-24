from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}/qos")
async def vif_get_qos_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
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


@router.get("/{cluster_id}/vif/{vif_uuid}/qos/type")
async def vif_get_qos_type_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS Type by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

    if vif is not None:
        ret = dict(success=True, data=vif.get_qos_type())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vif/{vif_uuid}/qos/speed")
async def vif_get_qos_speed_by_uuid(cluster_id: str, vif_uuid: str):
    """ Set VIF QoS Type by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

    if vif is not None:
        ret = dict(success=True, data=vif.get_qos_info()["kbps"])
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vif/{vif_uuid}/qos/speed/{speed}")
async def vif_set_qos_speed_by_uuid(
    cluster_id: str, vif_uuid: str, speed: str
):
    """ Set VIF QoS Speed by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
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

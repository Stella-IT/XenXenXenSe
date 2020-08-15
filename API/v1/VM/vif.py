from fastapi import APIRouter

from API.v1.Interface import NameArgs
from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

from ..VIF.serialize import serialize as _vif_serialize

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vif")
async def instance_vif(cluster_id: str, vm_uuid: str):
    """ Show Instnace VIFs """

    from XenXenXenSe.VIF import VIF

    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        new_vif = vm.get_VIF()

        if new_vif is not None:

            ret = {"success": True, "data": _vif_serialize(new_vif)}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/vif/qos")
async def vif_get_qos_by_uuid(cluster_id: str, vm_uuid: str):
    """ Set VIF QoS by VM """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        vif = vm.get_VIF()

        if vif is not None:
            ret = {
                "success": True,
                "data": {
                    "type": vif.get_qos_type(),
                    "info": vif.get_qos_info(),
                },
            }
        else:
            ret = {"success": False}

    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/vif/qos/speed/{speed}")
async def vif_set_qos_speed_by_vm(cluster_id: str, vm_uuid: str, speed: str):
    """ Set VIF QoS Speed by VM """
    from XenXenXenSe.VIF import VIF

    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        vif = vm.get_VIF()

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

                ret = {"success": vif.set_qos_info({"kbps": speed})}
            else:
                ret = {"success": False}

    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/vifs")
async def instance_vifs(cluster_id: str, vm_uuid: str):
    """ Show Instnace VIFs """

    from XenXenXenSe.VIF import VIF

    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        new_vifs = vm.get_VIFs()

        vif_serialized = []

        if new_vifs is not None:
            for vif in new_vifs:
                if vif is not None:
                    vif_serialized.append(_vif_serialize(vif))

            ret = {"success": True, "data": vif_serialized}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

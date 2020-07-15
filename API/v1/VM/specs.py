from fastapi import APIRouter

from API.v1.Interface import VCpuArgs, MemoryArgs
from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

from MySQL.VM import vm

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vCPU")
async def vm_get_vCPU(cluster_id: str, vm_uuid: str):
    """ Get VM vCPU count """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": True, "data": _vm.get_vCPUs()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/vCPU/params")
async def vm_get_vCPU_params(cluster_id: str, vm_uuid: str):
    """ Get vCPU Parameters """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": True, "data": _vm.get_vCPU_params()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.put("/{cluster_id}/vm/{vm_uuid}/vCPU")
async def vm_set_vCPU(cluster_id: str, vm_uuid: str, args: VCpuArgs):
    """ Set VM vCPU count """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_vCPUs(args.vCPU_count)}
    else:
        ret = {"success": False}

    vm.update_vm(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/vCPU/{vCPU_count}")
async def vm_set_vCPU_inurl(cluster_id: str, vm_uuid: str, vCPU_count: int):
    """ Set VM vCPU count """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_vCPUs(vCPU_count)}
    else:
        ret = {"success": False}

    vm.update_vm(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


# TODO: Trouble shooting required.
@router.get("/{cluster_id}/vm/{vm_uuid}/memory")
async def vm_get_memory(cluster_id: str, vm_uuid: str):
    """ Get VM Memory (needs troubleshooting) """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": True, "data": _vm.get_memory()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.put("/{cluster_id}/vm/{vm_uuid}/memory")
async def vm_set_memory(cluster_id: str, vm_uuid: str, args: MemoryArgs):
    """ Set VM Memory (needs troubleshooting) """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_memory(args.memory)}
    else:
        ret = {"success": False}

    vm.update_vm(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/memory/{memory_size}")
async def vm_set_memory_inurl(cluster_id: str, vm_uuid: str, memory_size: int):
    """ Set VM Memory (needs troubleshooting) """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_memory(memory_size)}
    else:
        ret = {"success": False}

    vm.update_vm(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret

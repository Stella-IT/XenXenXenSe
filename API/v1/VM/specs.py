from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Interface import MemoryArgs, VCpuArgs
from config import get_xen_clusters
from MySQL.VM import XenVm

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vCPU")
async def vm_get_vCPU(cluster_id: str, vm_uuid: str):
    """ Get VM vCPU count """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=True, data=_vm.get_vCPUs())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/vCPU/params")
async def vm_get_vCPU_params(cluster_id: str, vm_uuid: str):
    """ Get vCPU Parameters """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=True, data=_vm.get_vCPU_params())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.put("/{cluster_id}/vm/{vm_uuid}/vCPU")
async def vm_set_vCPU(cluster_id: str, vm_uuid: str, args: VCpuArgs):
    """ Set VM vCPU count """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.set_vCPUs(args.vCPU_count))
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/vCPU/{vCPU_count}")
async def vm_set_vCPU_inurl(cluster_id: str, vm_uuid: str, vCPU_count: int):
    """ Set VM vCPU count """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.set_vCPUs(vCPU_count))
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


# TODO: Trouble shooting required.
@router.get("/{cluster_id}/vm/{vm_uuid}/memory")
async def vm_get_memory(cluster_id: str, vm_uuid: str):
    """ Get VM Memory (needs troubleshooting) """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=True, data=_vm.get_memory())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.put("/{cluster_id}/vm/{vm_uuid}/memory")
async def vm_set_memory(cluster_id: str, vm_uuid: str, args: MemoryArgs):
    """ Set VM Memory (needs troubleshooting) """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.set_memory(args.memory))
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/memory/{memory_size}")
async def vm_set_memory_inurl(cluster_id: str, vm_uuid: str, memory_size: int):
    """ Set VM Memory (needs troubleshooting) """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.set_memory(memory_size))
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret

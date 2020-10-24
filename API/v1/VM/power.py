from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VM import VM

from config import get_xen_clusters
from MySQL.VM import XenVm

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/power")
async def vm_power(cluster_id: str, vm_uuid: str):
    """ Get VM's power status, Can be "Paused", "Halted", "Running" """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if _vm is not None:
        ret = dict(success=True, data=_vm.get_power_state())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/on")
async def vm_start(cluster_id: str, vm_uuid: str):
    """Start the VM
    System powerstate must be checked beforehand"""
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if XenVm is not None:
        ret = dict(success=_vm.start())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/off")
async def vm_shutdown(cluster_id: str, vm_uuid: str):
    """Shutdown VM, can return false if the system does not support ACPI shutdown.
    System powerstate must be checked beforehand"""

    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.shutdown())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/force_off")
async def vm_power_force_shutdown(cluster_id: str, vm_uuid: str):
    """ Force Shutdown the VM """

    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.force_shutdown())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/reboot")
async def vm_power_restart(cluster_id: str, vm_uuid: str):
    """Restart VM, can return false if the system does not support ACPI shutdown.
    System powerstate must be checked beforehand"""
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.reboot())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/suspend")
async def vm_power_suspend(cluster_id: str, vm_uuid: str):
    """ Suspend the VM """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.suspend())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/resume")
async def vm_power_resume(cluster_id: str, vm_uuid: str):
    """ Resume the VM """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.resume())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/pause")
async def vm_power_pause(cluster_id: str, vm_uuid: str):
    """ Pause the VM """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.pause())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/unpause")
async def vm_power_unpause(cluster_id: str, vm_uuid: str):
    """ Unpause the VM """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.unpause())
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=_vm)

    session.xenapi.session.logout()
    return ret

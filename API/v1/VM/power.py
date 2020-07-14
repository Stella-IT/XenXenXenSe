from fastapi import APIRouter

from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

from MySQL.VM import update_vm

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/power")
async def vm_power(cluster_id: str, vm_uuid: str):
    """ Get VM's power status, Can be "Paused", "Halted", "Running" """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:
        ret = {"success": True, "data": vm.get_power_state()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/on")
async def vm_start(cluster_id: str, vm_uuid: str):
    """ Start the VM
        System powerstate must be checked beforehand """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.start()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/off")
async def vm_shutdown(cluster_id: str, vm_uuid: str):
    """ Shutdown VM, can return false if the system does not support ACPI shutdown.
        System powerstate must be checked beforehand """

    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.shutdown()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/force_off")
async def vm_power_force_shutdown(cluster_id: str, vm_uuid: str):
    """ Force Shutdown the VM """

    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.force_shutdown()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/reboot")
async def vm_power_restart(cluster_id: str, vm_uuid: str):
    """ Restart VM, can return false if the system does not support ACPI shutdown.
        System powerstate must be checked beforehand """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.reboot()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/suspend")
async def vm_power_suspend(cluster_id: str, vm_uuid: str):
    """ Suspend the VM """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.suspend()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/resume")
async def vm_power_resume(cluster_id: str, vm_uuid: str):
    """ Resume the VM """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.resume()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/power/pause")
async def vm_power_pause(cluster_id: str, vm_uuid: str):
    """ Pause the VM """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.pause()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/vm/{vm_uuid}/power/unpause")
async def vm_power_unpause(cluster_id: str, vm_uuid: str):
    """ Unpause the VM """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": vm.unpause()}
    else:
        ret = {"success": False}

    update_vm(cluster_id, vm)

    session.xenapi.session.logout()
    return ret

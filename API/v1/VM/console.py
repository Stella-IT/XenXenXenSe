from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from ..Console.serialize import serialize as _console_serialize

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/console")
async def vm_console(cluster_id: str, vm_uuid: str):
    """ Get the first console of the VM """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        consoles = vm.get_consoles()
        ret = {"success": True, "data": _console_serialize(consoles[0])}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/consoles")
async def vm_consoles(cluster_id: str, vm_uuid: str):
    """ Get all consoles are available to the VM """

    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        consoles = vm.get_consoles()

        consoleList = []
        for console in consoles:
            consoleList.append(_console_serialize(console))

        ret = {"success": True, "data": consoleList}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

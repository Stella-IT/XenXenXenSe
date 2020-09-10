from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from API.v1.Console.serialize import serialize as _console_serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/console")
async def vm_console(cluster_id: str, vm_uuid: str):
    """ Get the first console of the VM """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        consoles = vm.get_consoles()
        ret = dict(success=True, data=_console_serialize(consoles[0]))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/consoles")
async def vm_consoles(cluster_id: str, vm_uuid: str):
    """ Get all consoles are available to the VM """

    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        consoles = vm.get_consoles()

        __consoleList = []
        consoleList = __consoleList.append
        for console in consoles:
            consoleList(_console_serialize(console))

        ret = dict(success=True, data=__consoleList)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

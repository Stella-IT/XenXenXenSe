from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from MySQL.VM import XenVm

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/delete")
@router.delete("/{cluster_id}/vm/{vm_uuid}")
async def vm_delete(cluster_id: str, vm_uuid: str):
    """ Delete VM """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.delete()}
    else:
        ret = {"success": False}

    await XenVm.remove_orphaned(cluster_id)

    session.xenapi.session.logout()
    return ret

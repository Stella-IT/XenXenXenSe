from fastapi import APIRouter

from API.v1.Interface import NameArgs
from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

from MySQL.VM import XenVm
from .serialize import serialize

router = APIRouter()


# @_clone.post("/{cluster_id}/_vm/{vm_uuid}/clone")


@router.post("/{cluster_id}/template/{vm_uuid}/clone")
async def instance_clone(cluster_id: str, vm_uuid: str, args: NameArgs):
    """ Clone Instance (VM/Template) """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        new_vm = _vm.clone(args.name)
        if new_vm is not None:
            ret = {"success": True, "data": serialize(new_vm)}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/template/{vm_uuid}/clone/{clone_name}")
async def instance_clone_inurl(cluster_id: str, vm_uuid: str, clone_name: str):
    """ Clone Instance (VM/Template) """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        new_vm = _vm.clone(clone_name)
        if new_vm is not None:
            ret = {"success": True, "data": serialize(new_vm)}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    XenVm.update(cluster_id, newVM)

    session.xenapi.session.logout()
    return ret

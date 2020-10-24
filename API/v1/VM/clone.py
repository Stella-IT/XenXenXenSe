from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Interface import NameArgs
from API.v1.VM.serialize import serialize
from config import get_xen_clusters
from MySQL.VM import XenVm

router = APIRouter()


# @_clone.post("/{cluster_id}/_vm/{vm_uuid}/clone")


@router.post("/{cluster_id}/template/{vm_uuid}/clone")
async def instance_clone(cluster_id: str, vm_uuid: str, args: NameArgs):
    """ Clone Instance (VM/Template) """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        new_vm = _vm.clone(args.name)
        if new_vm is not None:
            ret = dict(success=True, data=serialize(new_vm))
        else:
            ret = dict(success=False)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/template/{vm_uuid}/clone/{clone_name}")
async def instance_clone_inurl(cluster_id: str, vm_uuid: str, clone_name: str):
    """ Clone Instance (VM/Template) """
    new_vm = None
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        new_vm = _vm.clone(clone_name)
        if new_vm is not None:
            ret = dict(success=True, data=serialize(new_vm))
        else:
            ret = dict(success=False)
    else:
        ret = dict(success=False)

    await XenVm().update(cluster_id=cluster_id, _vm=new_vm)

    session.xenapi.session.logout()
    return ret

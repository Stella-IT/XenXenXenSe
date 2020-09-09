from fastapi import APIRouter

from API.v1.Interface import NameArgs, DescriptionArgs
from XenGarden.VM import VM
from XenGarden.session import create_session

from MySQL.VM import XenVm

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/name")
@router.get("/{cluster_id}/template/{vm_uuid}/name")
async def instance_get_name(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) Name """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": True, "data": _vm.get_name()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/description")
@router.get("/{cluster_id}/template/{vm_uuid}/description")
async def instance_get_description(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) Description (needs troubleshooting) """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": True, "data": _vm.get_description()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.put("/{cluster_id}/vm/{vm_uuid}/name")
@router.put("/{cluster_id}/template/{vm_uuid}/name")
async def instance_set_name(cluster_id: str, vm_uuid: str, args: NameArgs):
    """ Set Instance (VM/Template) Name """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_name(args.name)}
    else:
        ret = {"success": False}

    await XenVm.update(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/name/{new_name}")
@router.get("/{cluster_id}/template/{vm_uuid}/name/{new_name}")
async def instance_set_name_inurl(
    cluster_id: str, vm_uuid: str, new_name: str
):
    """ Set Instance (VM/Template) Name """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_name(new_name)}
    else:
        ret = {"success": False}

    await XenVm.update(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret


@router.put("/{cluster_id}/vm/{vm_uuid}/description")
@router.put("/{cluster_id}/template/{vm_uuid}/description")
async def instance_set_description(
    cluster_id: str, vm_uuid: str, args: DescriptionArgs
):
    """ Set Instance (VM/Template) Description """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_description(args.description)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/description/{new_description}")
@router.get("/{cluster_id}/template/{vm_uuid}/description/{new_description}")
async def instance_set_description_inurl(
    cluster_id: str, vm_uuid: str, new_description: str
):
    """ Set Instance (VM/Template) Description """
    session = create_session(cluster_id)
    _vm: VM = VM.get_by_uuid(session, vm_uuid)
    if _vm is not None:
        ret = {"success": _vm.set_description(new_description)}
    else:
        ret = {"success": False}

    await XenVm.update(cluster_id, _vm)

    session.xenapi.session.logout()
    return ret

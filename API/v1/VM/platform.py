from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/platform")
@router.get("/{cluster_id}/template/{vm_uuid}/platform")
async def instance_get_platform(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) Platform """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        ret = dict(success=True, data=vm.get_platform())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/platform/{name}")
@router.get("/{cluster_id}/template/{vm_uuid}/platform/{name}")
async def instance_set_platform_property_byname(
    cluster_id: str, vm_uuid: str, name: str
):
    """ Get Instance (VM/Template) Platform Property by Name """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        ret = dict(success=True, data=vm.get_platform()[name])
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/platform/{name}/{var}")
@router.get("/{cluster_id}/template/{vm_uuid}/platform/{name}/{var}")
async def instance_set_platform_property_byname_inurl(
    cluster_id: str, vm_uuid: str, name: str, var: str
):
    """ Set Instance (VM/Template) Platform Property by Name """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if vm is not None:
        data = {name: var}

        ret = dict(success=vm.set_platform(data))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

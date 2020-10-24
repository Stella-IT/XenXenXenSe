from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VM import VM

from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/bios")
@router.get("/{cluster_id}/template/{vm_uuid}/bios")
async def instance_get_bios(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) BIOS """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        ret = dict(success=True, data=vm.get_bios_strings())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/bios/{name}")
@router.get("/{cluster_id}/template/{vm_uuid}/bios/{name}")
async def instance_set_bios_property_byname(
    cluster_id: str, vm_uuid: str, name: str
):
    """ Get Instance (VM/Template) BIOS Property by Name """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        ret = dict(success=True, data=vm.get_bios_strings()[name])
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/bios/{name}/{var}")
@router.get("/{cluster_id}/template/{vm_uuid}/bios/{name}/{var}")
async def instance_set_bios_property_byname_inurl(
    cluster_id: str, vm_uuid: str, name: str, var: str
):
    """ Set Instance (VM/Template) BIOS Property by Name """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        data = {name: var}

        ret = dict(success=vm.set_bios_strings(data))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

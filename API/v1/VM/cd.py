from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from API.v1.VBD.serialize import serialize as _vbd_serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/cd")
async def get_cd(cluster_id: str, vm_uuid: str):
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())

    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if vm is not None:

        new_vbd = vm.get_CD()

        if new_vbd is not None:
            ret = dict(success=True, data=_vbd_serialize(new_vbd))
        else:
            ret = dict(success=False)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/cd/insert/{vdi_uuid}")
async def get_cd_insert_inurl(cluster_id: str, vm_uuid: str, vdi_uuid: str):
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())

    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if vm is not None:

        new_vbd = vm.get_CD()

        if new_vbd is not None:

            from XenGarden.VDI import VDI
            from API.v1.VDI.serialize import serialize as _vdi_serialize

            vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)

            if vdi is not None:
                success = new_vbd.insert(vdi)

                if success:
                    ret = dict(success=success, data=_vdi_serialize(vdi))
                else:
                    ret = dict(success=success)
            else:
                ret = dict(success=False)
        else:
            ret = dict(success=False)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.delete("/{cluster_id}/vm/{vm_uuid}/cd/insert")
@router.get("/{cluster_id}/vm/{vm_uuid}/cd/eject")
async def get_cd_eject(cluster_id: str, vm_uuid: str):
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())

    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if vm is not None:

        new_vbd = vm.get_CD()

        if new_vbd is not None:
            success = new_vbd.eject()

            ret = dict(success=success)
        else:
            ret = dict(success=False)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/cds")
async def get_cds(cluster_id: str, vm_uuid: str):
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())

    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if vm is not None:

        new_vbds = vm.get_CDs()

        __vbd_serialized = []
        vbd_serialized = __vbd_serialized.append
        if new_vbds is not None:
            for vbd in new_vbds:
                if vbd is not None:
                    vbd_serialized(_vbd_serialize(vbd))

            ret = dict(success=True, data=__vbd_serialized)
        else:
            ret = dict(success=False)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.delete("/{cluster_id}/vm/{VM_UUID}/cd")
@router.get("/{cluster_id}/vm/{VM_UUID}/cd/eject")
@router.get("/{cluster_id}/vm/{VM_UUID}/cd/remove")
async def remove_cd(cluster_id: str, vm_uuid: str):
    pass

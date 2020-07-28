from fastapi import APIRouter

from XenXenXenSe.VM import VM
from XenXenXenSe.SR import SR
from XenXenXenSe.session import create_session

from ..VBD.serialize import serialize as _vbd_serialize

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/cd")
async def get_cd(cluster_id: str, vm_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        new_vbd = vm.get_CD()

        if new_vbd is not None:
            ret = {"success": True, "data": _vbd_serialize(vbd)}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/vm/{vm_uuid}/cd/insert/{vdi_uuid}")
async def get_cd_insert_inurl(cluster_id: str, vm_uuid: str, vdi_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        new_vbd = vm.get_CD()

        if new_vbd is not None:

            from XenXenXenSe.VDI import VDI
            from ..VDI.serialize import serialize as _vdi_serialize

            vdi: VDI = VDI.get_by_uuid(session, vdi_uuid)

            if vdi is not None:
                success = new_vbd.insert(vdi)

                if success:
                    ret = {"success": success, "data": _vdi_serialize(vdi)}
                else:
                    ret = {"success": success}
            else:
                ret = {"success": False}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.delete("/{cluster_id}/vm/{vm_uuid}/cd/insert")
@router.get("/{cluster_id}/vm/{vm_uuid}/cd/eject")
async def get_cd_eject(cluster_id: str, vm_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        new_vbd = vm.get_CD()

        if new_vbd is not None:
            success = new_vbd.eject()

            ret = {"success": success}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/vm/{vm_uuid}/cds")
async def get_cds(cluster_id: str, vm_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        new_vbds = vm.get_CDs()

        vbd_serialized = []

        if new_vbds is not None:
            for vbd in new_vbds:
                if vbd is not None:
                    vbd_serialized.append(_vbd_serialize(vbd))

            ret = {"success": True, "data": vbd_serialized}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret




@router.delete("/{cluster_id}/vm/{VM_UUID}/cd")
@router.get("/{cluster_id}/vm/{VM_UUID}/cd/eject")
@router.get("/{cluster_id}/vm/{VM_UUID}/cd/remove")
async def remove_cd(cluster_id: str, vm_uuid: str):
    pass

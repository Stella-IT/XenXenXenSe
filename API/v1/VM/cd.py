from fastapi import APIRouter

from XenXenXenSe.VM import VM
from XenXenXenSe.SR import SR
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/_vm/{vm_uuid}/cd")
async def get_cd(cluster_id: str, vm_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        newVBD = vm.get_CD()

        if newVBD is not None:
            ret = {"success": True, "data": newVBD.serialize()}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/_vm/{vm_uuid}/cd/insert/{vdi_uuid}")
async def get_cd_insert_inurl(cluster_id: str, vm_uuid: str, vdi_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        newVBD = vm.get_CD()

        if newVBD is not None:

            from XenXenXenSe.VDI import VDI

            vdi: VDI = VDI.get_by_uuid(session, vdi_uuid)

            if vdi is not None:
                success = newVBD.insert(vdi)

                if success:
                    ret = {"success": success, "data": vdi.serialize()}
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

@router.delete("/{cluster_id}/_vm/{vm_uuid}/cd/insert")
@router.get("/{cluster_id}/_vm/{vm_uuid}/cd/eject")
async def get_cd_eject(cluster_id: str, vm_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        newVBD = vm.get_CD()

        if newVBD is not None:
            success = newVBD.eject()

            ret = {"success": success}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/_vm/{vm_uuid}/cds")
async def get_cds(cluster_id: str, vm_uuid: str):
    session = create_session(cluster_id)

    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        newVBDs = vm.get_CDs()

        vbd_serialized = []

        if newVBDs is not None:
            for vbd in newVBDs:
                if vbd is not None:
                    vbd_serialized.append(vbd.serialize())

            ret = {"success": True, "data": vbd_serialized}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret




@router.delete("/{cluster_id}/_vm/{VM_UUID}/cd")
@router.get("/{cluster_id}/_vm/{VM_UUID}/cd/eject")
@router.get("/{cluster_id}/_vm/{VM_UUID}/cd/remove")
async def remove_cd(cluster_id: str, vm_uuid: str):
    pass

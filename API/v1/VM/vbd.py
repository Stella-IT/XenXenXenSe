from fastapi import APIRouter

from API.v1.Interface import NameArgs
from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vbd")
@router.get("/{cluster_id}/vm/{vm_uuid}/vbds")
async def instance_vbds(cluster_id: str, vm_uuid: str):
    """ Show Instance VBDs """

    from XenXenXenSe.VBD import VBD
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:

        newVBDs = vm.get_VBDs()

        vbd_serialized = []

        if newVBDs is not None:
            for vbd in newVBDs:
                if vbd is not None:
                    vbd_serialized.append(vbd.serialize())

            print(vbd_serialized)

            ret = {"success": True, "data": vbd_serialized}
        else:
            ret = {"success": False}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

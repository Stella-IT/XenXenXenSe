from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from API.v1.VBD.serialize import serialize as _vbd_serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vbd")
@router.get("/{cluster_id}/vm/{vm_uuid}/vbds")
async def instance_vbds(cluster_id: str, vm_uuid: str):
    """ Show Instance VBDs """
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if vm is not None:

        newVBDs = vm.get_VBDs()

        __vbd_serialized = []
        vbd_serialized = __vbd_serialized.append

        if newVBDs is not None:
            for vbd in newVBDs:
                if vbd is not None:
                    vbd_serialized(_vbd_serialize(vbd))

            print(__vbd_serialized)

            ret = dict(success=True, data=__vbd_serialized)
        else:
            ret = dict(success=False)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

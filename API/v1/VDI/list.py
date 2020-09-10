from fastapi import APIRouter

from XenGarden.VDI import VDI
from XenGarden.session import create_session

from API.v1.VDI.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vdi/list")
async def vdi_list(cluster_id: str):
    """ Get VDI by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vdis = VDI.get_all(session=session)

    __vdi_list = []
    _vdi_list = __vdi_list.append
    for vdi in vdis:
        _vdi_list(serialize(vdi))

    if vdis is not None:
        ret = dict(success=True, data=__vdi_list)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

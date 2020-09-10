from fastapi import APIRouter

from XenGarden.VIF import VIF
from XenGarden.session import create_session

from API.v1.VIF.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vif/list")
async def vif_list(cluster_id: str):
    """ Get All from Storage Repos """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vifs = VIF.get_all(session=session)

    __santilized_vifs = []
    santilized_vifs = __santilized_vifs.append
    for vif in vifs:
        santilized_vifs(serialize(vif))

    ret = dict(success=True, data=__santilized_vifs)

    session.xenapi.session.logout()
    return ret

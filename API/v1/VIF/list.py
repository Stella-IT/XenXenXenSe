from fastapi import APIRouter

from XenXenXenSe.VIF import VIF
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vif/list")
async def vif_list(cluster_id: str):
    """ Get All from Storage Repos """
    session = create_session(cluster_id)
    vifs = VIF.get_all(session)

    santilized_vifs = []
    for vif in vifs:
        santilized_vifs.append(vif.serialize())

    ret = {
        "success": True,
        "data": santilized_vifs
    }

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter

from XenGarden.VIF import VIF
from XenGarden.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}")
async def vif_get_by_uuid(cluster_id: str, vif_uuid: str):
    """ Get VIF by UUID """
    session = create_session(cluster_id)
    vif: VIF = VIF.get_by_uuid(session, vif_uuid)

    if vif is not None:
        ret = {"success": True, "data": serialize(vif)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter

from XenXenXenSe.SR import SR
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/sr/{sr_uuid}")
async def sr_get_by_uuid(cluster_id: str, sr_uuid: str):
    """ Get SR by UUID """
    session = create_session(cluster_id)
    sr: SR = SR.get_by_uuid(session, sr_uuid)

    if sr is not None:
        ret = {"success": True, "data": sr.serialize()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

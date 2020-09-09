from fastapi import APIRouter

from XenGarden.SR import SR
from XenGarden.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/sr/{sr_uuid}/scan")
async def sr_scan(cluster_id: str, sr_uuid: str):
    """ Scan Storage Repository """
    session = create_session(cluster_id)
    sr: SR = SR.get_by_uuid(session, sr_uuid)

    if sr is not None:
        sr.scan()
        ret = {"success": True}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

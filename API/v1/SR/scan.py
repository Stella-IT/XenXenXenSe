from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.SR import SR

from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/sr/{sr_uuid}/scan")
async def sr_scan(cluster_id: str, sr_uuid: str):
    """ Scan Storage Repository """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    sr: SR = SR.get_by_uuid(session=session, uuid=sr_uuid)

    if sr is not None:
        sr.scan()
        ret = dict(success=True)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

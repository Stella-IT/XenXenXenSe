from fastapi import APIRouter

from XenGarden.SR import SR
from XenGarden.session import create_session

from API.v1.SR.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/sr/{sr_uuid}")
async def sr_get_by_uuid(cluster_id: str, sr_uuid: str):
    """ Get SR by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    sr: SR = SR.get_by_uuid(session=session, uuid=sr_uuid)

    if sr is not None:
        ret = dict(success=True, data=serialize(sr))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

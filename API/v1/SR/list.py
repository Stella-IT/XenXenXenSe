from fastapi import APIRouter

from XenXenXenSe.SR import SR
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/sr/list")
async def sr_list(cluster_id: str):
    """ Get All from Storage Repos """
    session = create_session(cluster_id)
    srs = SR.get_all(session)

    sant_sr = []
    for sr in srs:
        sant_sr.append(sr.serialize())

    ret = {
        "success": True,
        "data": sant_sr
    }

    session.xenapi.session.logout()
    return ret

from fastapi import APIRouter

from API.v1.Interface import NameArgs

from XenGarden.SR import SR
from XenGarden.session import create_session

from API.v1.SR.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.post("/{cluster_id}/sr/find")
async def find_cd_by_name(cluster_id: str, args: NameArgs):
    """ Find SR by Name """
    sr = None
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    name = args.name
    srs = SR.get_by_name(session=session, name=name)

    __srs_list = []
    srs_list = __srs_list.append
    for sr in srs:
        srs_list(serialize(sr))

    if sr is not None:
        ret = dict(success=True, data=__srs_list)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/sr/find/{iso_name}")
async def insert_cd_inurl_name(cluster_id: str, iso_name: str):
    """ Find SR by Name """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    srs = SR.get_by_name(session=session, name=iso_name)

    if srs is not None:
        __srs_list = []
        srs_list = __srs_list.append
        for sr in srs:
            srs_list(serialize(sr))

        ret = dict(success=True, data=__srs_list)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

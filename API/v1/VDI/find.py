from fastapi import APIRouter

from API.v1.Interface import NameArgs

from XenGarden.VDI import VDI
from XenGarden.session import create_session

from API.v1.VDI.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.post("/{cluster_id}/vdi/find")
async def find_VDI_by_name(cluster_id: str, args: NameArgs):
    """ Find VDI by Name """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    name = args.name
    vdis = VDI.get_by_name(session=session, name=name)

    if vdis is not None:
        __vdis_list = []
        vdis_list = __vdis_list.append
        for vdi in vdis:
            vdis_list(serialize(vdi))

        ret = dict(success=True, data=__vdis_list)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vdi/find/{iso_name}")
async def insert_cd_inurl_name(cluster_id: str, iso_name: str):
    """ Find VDI by Name """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vdis = VDI.get_by_name(session=session, name=iso_name)
    print(vdis)

    if vdis is not None:
        __vdis_list = []
        vdis_list = __vdis_list.append
        for vdi in vdis:
            vdis_list(serialize(vdi))

        ret = dict(success=True, data=__vdis_list)
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

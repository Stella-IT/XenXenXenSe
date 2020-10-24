from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VBD import VBD
from XenGarden.VDI import VDI

from API.v1.Interface import UUIDArgs
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vbd/{vbd_uuid}/insert/{vdi_uuid}")
async def vbd_insert_vdi_by_uuid(
    cluster_id: str, vbd_uuid: str, vdi_uuid: str
):
    """ Insert VDI into VBD by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)

    if vdi is None:
        ret = dict(success=False)
        session.xenapi.session.logout()
        return ret

    vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

    if vbd is not None:
        ret = dict(success=vbd.insert(vdi))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.put("/{cluster_id}/vbd/{vbd_uuid}/insert")
async def vbd_insert_vdi_by_uuid(
    cluster_id: str, vbd_uuid: str, res: UUIDArgs
):
    """ Insert VDI into VBD by UUID """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vdi: VDI = VDI.get_by_uuid(session=session, uuid=res.uuid)

    if vdi is None:
        ret = dict(success=False)
        session.xenapi.session.logout()
        return ret

    vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

    if vbd is not None:
        ret = dict(success=vbd.insert(vdi))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.delete("/{cluster_id}/vbd/{vbd_uuid}/insert")
@router.get("/{cluster_id}/vbd/{vbd_uuid}/eject")
async def vbd_eject_vdi(cluster_id: str, vbd_uuid: str):
    """ Eject VDI from VBD """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

    if vbd is not None:
        ret = dict(success=vbd.eject())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret

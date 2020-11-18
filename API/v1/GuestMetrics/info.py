from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException, Path
from XenGarden.GuestMetrics import GuestMetrics
from XenGarden.Host import Host
from XenGarden.session import create_session

from API.v1.GuestMetrics.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/guest/{guest_uuid}")
async def guest_get_by_uuid(
    cluster_id: str = Path(default=None, title="cluster_id", description="Cluster ID"),
    guest_uuid: str = Path(default=None, title="guest_uuid", description="Guest UUID"),
):
    """ Get GuestMetrics by UUID """
    try:
        # KeyError Handling
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        guest: GuestMetrics = Host.get_by_uuid(session=session, uuid=guest_uuid)

        if guest is not None:
            ret = dict(success=True, data=serialize(guest))
        else:
            ret = dict(success=False)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

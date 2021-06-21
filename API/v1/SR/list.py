import asyncio
from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.SR import SR

from API.v1.Common import xenapi_failure_jsonify
from API.v1.SR.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/sr/list")
async def sr_list(cluster_id: str):
    """Get All from Storage Repos"""
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        srs = SR.get_all(session=session)
        __sant_sr = await asyncio.gather(*[serialize(sr) for sr in srs])

        ret = dict(success=True, data=__sant_sr)

        session.xenapi.session.logout()
        return ret
    except Failure as xenapi_error:
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)

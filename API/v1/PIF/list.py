import asyncio
from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.PIF import PIF
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.PIF.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/pif/list")
async def pif_list(cluster_id: str):
    """Get All PIF from cluster"""

    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        pifs = PIF.get_all(session=session)
        __santilized_pifs = await asyncio.gather(*[serialize(pif) for pif in pifs])

        ret = dict(success=True, data=__santilized_pifs)

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
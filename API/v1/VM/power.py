from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/power")
async def vm_power(cluster_id: str, vm_uuid: str):
    """Get VM's power status, Can be "Paused", "Halted", "Running" """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        ret = dict(success=True, data=_vm.get_power_state())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/on")
async def vm_start(cluster_id: str, vm_uuid: str):
    """Start the VM
    System powerstate must be checked beforehand"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.start())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/off")
async def vm_shutdown(cluster_id: str, vm_uuid: str):
    """Shutdown VM, can return false if the system does not support ACPI shutdown.
    System powerstate must be checked beforehand"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.shutdown())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/force_off")
async def vm_power_force_shutdown(cluster_id: str, vm_uuid: str):
    """Force Shutdown the VM"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.force_shutdown())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/reboot")
async def vm_power_restart(cluster_id: str, vm_uuid: str):
    """Restart VM, can return false if the system does not support ACPI shutdown.
    System powerstate must be checked beforehand"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.reboot())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/suspend")
async def vm_power_suspend(cluster_id: str, vm_uuid: str):
    """Suspend the VM"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.suspend())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/resume")
async def vm_power_resume(cluster_id: str, vm_uuid: str):
    """Resume the VM"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.resume())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/pause")
async def vm_power_pause(cluster_id: str, vm_uuid: str):
    """Pause the VM"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.pause())

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


@router.get("/{cluster_id}/vm/{vm_uuid}/power/unpause")
async def vm_power_unpause(cluster_id: str, vm_uuid: str):
    """Unpause the VM"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=await _vm.unpause())

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

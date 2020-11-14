from fastapi import APIRouter

from API.v1.Host.info import router as _host_info
from API.v1.Host.list import router as _host_list
from API.v1.SR.find import router as _sr_find
from API.v1.SR.info import router as _sr_info
from API.v1.SR.list import router as _sr_list
from API.v1.SR.scan import router as _sr_scan
from API.v1.VBD.delete import router as _vbd_delete
from API.v1.VBD.find_vdi import router as _vbd_find_by_vdi
from API.v1.VBD.info import router as _vbd_info
from API.v1.VBD.list import router as _vbd_list
from API.v1.VBD.media import router as _vbd_media
from API.v1.VBD.plug import router as _vbd_plug
from API.v1.VDI.delete import router as _vdi_delete
from API.v1.VDI.find import router as _vdi_find
from API.v1.VDI.info import router as _vdi_info
from API.v1.VDI.list import router as _vdi_list
from API.v1.VIF.info import router as _vif_info
from API.v1.VIF.list import router as _vif_list
from API.v1.VIF.qos import router as _vif_qos
from API.v1.VM.bios import router as _vm_bios
from API.v1.VM.cd import router as _vm_cd
from API.v1.VM.clone import router as _vm_clone
from API.v1.VM.console import router as _vm_console
from API.v1.VM.delete import router as _vm_delete
from API.v1.VM.guest import router as _vm_guest
from API.v1.VM.info import router as _vm_info
from API.v1.VM.list import router as _vm_list
from API.v1.VM.metadata import router as _vm_metadata
from API.v1.VM.platform import router as _vm_platform
from API.v1.VM.power import router as _vm_power
from API.v1.VM.specs import router as _vm_specs
from API.v1.VM.vbd import router as _vm_vbd
from API.v1.VM.vif import router as _vm_vif

router = APIRouter()

_prefix = "/v1"

router.include_router(_host_list, prefix=_prefix, tags=["host"])
router.include_router(_host_info, prefix=_prefix, tags=["host"])

router.include_router(_vm_clone, prefix=_prefix, tags=["vm"])
router.include_router(_vm_cd, prefix=_prefix, tags=["vm"])
router.include_router(_vm_console, prefix=_prefix, tags=["vm"])
router.include_router(_vm_delete, prefix=_prefix, tags=["vm"])
router.include_router(_vm_guest, prefix=_prefix, tags=["vm"])
router.include_router(_vm_list, prefix=_prefix, tags=["vm"])
router.include_router(_vm_info, prefix=_prefix, tags=["vm"])
router.include_router(_vm_metadata, prefix=_prefix, tags=["vm"])
router.include_router(_vm_platform, prefix=_prefix, tags=["vm"])
router.include_router(_vm_power, prefix=_prefix, tags=["vm"])
router.include_router(_vm_specs, prefix=_prefix, tags=["vm"])
router.include_router(_vm_vbd, prefix=_prefix, tags=["vm"])
router.include_router(_vm_vif, prefix=_prefix, tags=["vm"])
router.include_router(_vm_bios, prefix=_prefix, tags=["vm"])

router.include_router(_sr_list, prefix=_prefix, tags=["sr"])
router.include_router(_sr_find, prefix=_prefix, tags=["sr"])
router.include_router(_sr_info, prefix=_prefix, tags=["sr"])
router.include_router(_sr_scan, prefix=_prefix, tags=["sr"])

router.include_router(_vbd_list, prefix=_prefix, tags=["vbd"])
router.include_router(_vbd_info, prefix=_prefix, tags=["vbd"])
router.include_router(_vbd_find_by_vdi, prefix=_prefix, tags=["vbd"])
router.include_router(_vbd_media, prefix=_prefix, tags=["vbd"])
router.include_router(_vbd_plug, prefix=_prefix, tags=["vbd"])
router.include_router(_vbd_delete, prefix=_prefix, tags=["vbd"])

router.include_router(_vdi_list, prefix=_prefix, tags=["vdi"])
router.include_router(_vdi_find, prefix=_prefix, tags=["vdi"])
router.include_router(_vdi_info, prefix=_prefix, tags=["vdi"])
router.include_router(_vdi_delete, prefix=_prefix, tags=["vdi"])

router.include_router(_vif_list, prefix=_prefix, tags=["vif"])
router.include_router(_vif_info, prefix=_prefix, tags=["vif"])
router.include_router(_vif_qos, prefix=_prefix, tags=["vif"])


@router.get("/", status_code=404)
async def root_dir():
    return {
        "status_code": 404
    }
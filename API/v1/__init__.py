from fastapi import APIRouter

from .Host.list import router as _host_list
from .Host.info import router as _host_info

from .SR.list import router as _sr_list
from .SR.find import router as _sr_find
from .SR.info import router as _sr_info
from .SR.scan import router as _sr_scan

from .VBD.delete import router as _vbd_delete
from .VBD.info import router as _vbd_info
from .VBD.list import router as _vbd_list
from .VBD.find_vdi import router as _vbd_find_by_vdi
from .VBD.media import router as _vbd_media
from .VBD.plug import router as _vbd_plug

from .VDI.list import router as _vdi_list
from .VDI.find import router as _vdi_find
from .VDI.info import router as _vdi_info
from .VDI.delete import router as _vdi_delete

from .VIF.list import router as _vif_list
from .VIF.info import router as _vif_info
from .VIF.qos import router as _vif_qos

from .VM.bios import router as _vm_bios
from .VM.clone import router as _vm_clone
from .VM.cd import router as _vm_cd
from .VM.console import router as _vm_console
from .VM.delete import router as _vm_delete
from .VM.guest import router as _vm_guest
from .VM.info import router as _vm_info
from .VM.list import router as _vm_list
from .VM.metadata import router as _vm_metadata
from .VM.platform import router as _vm_platform
from .VM.power import router as _vm_power
from .VM.specs import router as _vm_specs
from .VM.vbd import router as _vm_vbd
from .VM.vif import router as _vm_vif

router = APIRouter()

_prefix = "/v1"

router.include_router(_host_list, prefix=_prefix, tags=['host'])
router.include_router(_host_info, prefix=_prefix, tags=['host'])

router.include_router(_vm_clone, prefix=_prefix, tags=['vm'])
router.include_router(_vm_cd, prefix=_prefix, tags=['vm'])
router.include_router(_vm_console, prefix=_prefix, tags=['vm'])
router.include_router(_vm_delete, prefix=_prefix, tags=['vm'])
router.include_router(_vm_guest, prefix=_prefix, tags=['vm'])
router.include_router(_vm_list, prefix=_prefix, tags=['vm'])
router.include_router(_vm_info, prefix=_prefix, tags=['vm'])
router.include_router(_vm_metadata, prefix=_prefix, tags=['vm'])
router.include_router(_vm_platform, prefix=_prefix, tags=['vm'])
router.include_router(_vm_power, prefix=_prefix, tags=['vm'])
router.include_router(_vm_specs, prefix=_prefix, tags=['vm'])
router.include_router(_vm_vbd, prefix=_prefix, tags=['vm'])
router.include_router(_vm_vif, prefix=_prefix, tags=['vm'])
router.include_router(_vm_bios, prefix=_prefix, tags=['vm'])

router.include_router(_sr_list, prefix=_prefix, tags=['sr'])
router.include_router(_sr_find, prefix=_prefix, tags=['sr'])
router.include_router(_sr_info, prefix=_prefix, tags=['sr'])
router.include_router(_sr_scan, prefix=_prefix, tags=['sr'])

router.include_router(_vbd_list, prefix=_prefix, tags=['vbd'])
router.include_router(_vbd_info, prefix=_prefix, tags=['vbd'])
router.include_router(_vbd_find_by_vdi, prefix=_prefix, tags=['vbd'])
router.include_router(_vbd_media, prefix=_prefix, tags=['vbd'])
router.include_router(_vbd_plug, prefix=_prefix, tags=['vbd'])
router.include_router(_vbd_delete, prefix=_prefix, tags=['vbd'])

router.include_router(_vdi_list, prefix=_prefix, tags=['vdi'])
router.include_router(_vdi_find, prefix=_prefix, tags=['vdi'])
router.include_router(_vdi_info, prefix=_prefix, tags=['vdi'])
router.include_router(_vdi_delete, prefix=_prefix, tags=['vdi'])

router.include_router(_vif_list, prefix=_prefix, tags=['vif'])
router.include_router(_vif_info, prefix=_prefix, tags=['vif'])
router.include_router(_vif_qos, prefix=_prefix, tags=['vif'])

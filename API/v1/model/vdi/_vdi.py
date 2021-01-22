from typing import List, Optional

from pydantic import BaseModel


class _vdi_list(BaseModel):
    name: str
    description: str
    uuid: str
    location: str
    type: str


class VDLResponseModel(BaseModel):
    """
    {
      "success": true,
      "data": [
        {
          "name": "guest-tools.iso",
          "description": "",
          "uuid": "b79fc9b4-2f16-440c-b76e-790c063500b4",
          "location": "guest-tools-7.45.0-2.xcpng8.1.iso",
          "type": "user"
        },
        {
          "name": "SCSI 1:0:0:0",
          "description": "QEMU model QEMU DVD-ROM rev 2.5+ type 5",
          "uuid": "4a615bee-0848-4c84-9bd9-79a9438cacfe",
          "location": "/dev/xapi/cd/sr0",
          "type": "user"
        }
      ]
    }
    """

    success: bool
    data: List[Optional[_vdi_list]]


class VDIFindResponseModel(BaseModel):
    success: bool
    data: List[Optional[_vdi_list]]


class VDInfoResponseModel(BaseModel):
    success: bool
    data: Optional[_vdi_list]


class VDIDelResponseModel(BaseModel):
    success: bool

from typing import Optional

from pydantic import BaseModel


class _memory(BaseModel):
    free: int
    total: int


class _cpu(BaseModel):
    """
    "cpu": {
      "cpu_count": "1",
      "socket_count": "1",
      "vendor": "GenuineIntel",
      "speed": "2594.018",
      "modelname": "Intel Xeon Processor (Skylake, IBRS)",
      "family": "6",
      "model": "85",
      "stepping": "4",
      "flags": "fpu de tsc msr pae mce cx8 apic sep mca cmov pat clflush mmx fxsr sse sse2 syscall nx rdtscp lm constant_tsc rep_good nopl cpuid pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm cpuid_fault ssbd ibrs ibpb stibp fsgsbase bmi1 hle avx2 bmi2 erms rtm clwb xsaveopt",
      "features": "fffa3203-078bfbff-00000021-2c100800",
      "features_pv": "1789cbf5-f6f83203-2991cbf5-00000023-00000001-01000b39-00000000-00000000-00001000-8c000000-00000000-00000000-00000000-00000000-00000000",
      "features_hvm": "10000000-00200000-00000000-00000402-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000",
      "features_hvm_host": "10000000-00200000-00000000-00000402-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000-00000000",
      "features_pv_host": "1789cbf5-f6f83203-2991cbf5-00000023-00000001-01000b39-00000000-00000000-00001000-8c000000-00000000-00000000-00000000-00000000-00000000"
    },

    """

    cpu_count: int
    socket_count: int
    vendor: str
    speed: float
    modelname: str
    family: int
    model: int
    stepping: int
    flags: str
    features: str
    features_pv: str
    features_hvm: str
    features_hvm_host: str
    features_pv_host: str


class _bios(BaseModel):
    """
    "bios_vendor": "Vultr",
    "bios_version": "",
    "system_manufacturer": "Vultr",
    "system_product_name": "VC2",
    "system_version": "pc-i440fx-4.1",
    "system_serial_number": "41921856",
    "baseboard_manufacturer": "",
    "baseboard_product_name": "",
    "baseboard_version": "",
    "baseboard_serial_number": "",
    "oem_1": "Xen",
    "oem_2": "MS_VM_CERT/SHA1/bdbeb6e0a816d43fa6d3fe8aaef04c2bad9d3e3d",
    "hp_rombios": ""
    """

    bios_vendor: str
    bios_version: str
    system_manufacturer: str
    system_product_name: str
    system_version: str
    system_serial_number: int
    baseboard_manufacturer: str
    baseboard_product_name: str
    baseboard_version: str
    baseboard_serial_number: int
    oem_1: str
    oem_2: str


class _InternalGHU(BaseModel):
    uuid: str
    name: str
    description: str
    enabled: bool
    memory: Optional[_memory]
    cpu: Optional[_cpu]
    bios: Optional


class GHUResponseModel(BaseModel):
    success: bool
    data: Optional[_InternalGHU]

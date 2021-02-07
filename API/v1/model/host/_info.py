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

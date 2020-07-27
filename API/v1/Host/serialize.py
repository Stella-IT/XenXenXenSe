from XenXenXenSe.Host import Host

def serialize(host: Host):
    return {
        "uuid": host.get_uuid(),
        "name": host.get_name(),
        "description": host.get_description(),
        "enabled": host.get_enabled(),
        "memory": {
            "free": host.get_free_memory(),
            "total": host.get_total_memory()
        },
        "cpu": host.get_cpu_info(),
        "bios": host.get_bios_strings(),
        "version": host.get_software_version(),
    }

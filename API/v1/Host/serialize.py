from XenGarden.Host import Host


def replace_under_bar(t):
    return dict((key.replace("-", "_"), value) for (key, value) in t.items())


def serialize(host: Host):
    return dict(
        uuid=host.get_uuid(),
        name=host.get_name(),
        description=host.get_description(),
        enabled=host.get_enabled(),
        memory=dict(free=host.get_free_memory(), total=host.get_total_memory()),
        cpu=host.get_cpu_info(),
        bios=replace_under_bar(host.get_bios_strings()),
        version=host.get_software_version(),
    )

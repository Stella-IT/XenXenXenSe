from XenGarden.Host import Host


def replace_under_bar(t):
    return dict((key.replace("-", "_"), value) for (key, value) in t.items())


async def serialize(host: Host):
    record = host.get_record()

    return dict(
        uuid=record["uuid"],
        name=record["name_label"],
        enabled=record["enabled"],
        memory=dict(
            overhead=record["memory_overhead"],
            free=host.get_free_memory(),
            total=host.get_total_memory(),
        ),
        cpu=record["cpu_info"],
        bios=record["bios_strings"],
        version=record["software_version"],
    )

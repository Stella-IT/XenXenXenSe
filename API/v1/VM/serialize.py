from XenGarden.VM import VM


async def serialize(vm: VM):
    record = vm.get_record()

    return dict(
        name=record["name_label"],
        bios=record["bios_strings"],
        power=record["power_state"],
        description=record["name_description"],
        uuid=record["uuid"],
        vCPUs=record["VCPUs_at_startup"],
        memory=vm.get_memory(),
    )

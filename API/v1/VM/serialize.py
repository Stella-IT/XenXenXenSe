from XenGarden.VM import VM


async def serialize(vm: VM):
    return dict(
        name=vm.get_name(),
        bios=vm.get_bios_strings(),
        power=vm.get_power_state(),
        description=vm.get_description(),
        uuid=vm.get_uuid(),
        vCPUs=vm.get_vCPUs(),
        memory=vm.get_memory(),
    )

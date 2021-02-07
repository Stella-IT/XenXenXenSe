from XenGarden.VBD import VBD


def serialize(vbd: VBD):
    from API.v1.VDI.serialize import serialize as _vdi_serialize
    from API.v1.VM.serialize import serialize as _vm_serialize

    vm = vbd.get_VM()
    vdi = vbd.get_VDI()

    if vm is not None:
        vm = _vm_serialize(vm)

    if vdi is not None:
        vdi = _vdi_serialize(vdi)

    return dict(
        vm=vm,
        vdi=vdi,
        bootable=vbd.get_bootable(),
        attached=vbd.get_currently_attached(),
        unpluggable=vbd.get_unpluggable(),
        device=vbd.get_device(),
        type=vbd.get_type(),
        uuid=vbd.get_uuid(),
        mode=vbd.get_mode(),
    )

class status:
    enabled = False

    @classmethod
    def get_enabled(cls) -> bool:
        return cls.enabled

    @classmethod
    def set_enabled(cls, _status: bool) -> None:
        cls.enabled = _status

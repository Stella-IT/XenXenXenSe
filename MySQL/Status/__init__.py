class status:
    enabled = False

    @classmethod
    def get_enabled(cls):
        return cls.enabled

    @classmethod
    def set_enabled(cls, _status):
        cls.enabled = _status

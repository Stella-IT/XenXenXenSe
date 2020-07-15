class status:
    enabled = False

    @classmethod
    def get_enabled(cls):
        return cls.enabled

    @classmethod
    def set_enabled(cls, status):
        cls.enabled = status

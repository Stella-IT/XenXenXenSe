class Console:
    """ The Virtual Console """

    def __init__(self, session, console):
        self.session = session
        self.console = console

    def serialize(self):
        return {
            "location": self.get_location(),
            "protocol": self.get_protocol(),
            "uuid": self.get_uuid(),
        }

    def get_location(self):
        """ The Location for Console """
        try:
            return self.session.xenapi.console.get_location(self.console)
        except Exception as e:
            print("Console.get_location Exception", e)
            return None

    def get_uuid(self):
        """ Returns UUID of Console """
        try:
            return self.session.xenapi.console.get_uuid(self.console)
        except Exception as e:
            print("Console.get_uuid Exception", e)
            return None

    def get_protocol(self):
        """ Returns Protocol of Console """
        try:
            return self.session.xenapi.console.get_protocol(self.console)
        except Exception as e:
            print("Console.get_protocol Exception", e)
            return None

    def get_VM(self):
        """ Returns which VM is this console attached to """
        try:
            return self.session.xenapi.console.get_VM(self.console)
        except Exception as e:
            print("Console.get_protocol Exception", e)
            return None
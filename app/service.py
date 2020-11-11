import uvicorn
from fastapi import FastAPI


class Server(FastAPI):
    def __init__(
        self,
        ctx,
        host: str,
        port: int,
        asgi_debug: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.controller = ctx

        # ASGI Server configuration parameters
        self.server = uvicorn
        self._host = host
        self._port = port
        self._asgi_debug = asgi_debug

        super(Server, self).__init__(*args, **kwargs)

    def make_process(self) -> None:
        return self.server.run(
            app=self, host=self._host, port=self._port, debug=self._asgi_debug
        )


# class Schedule:
#    def __init__(self):
#        self.terminating = False

    # def schedule_process(self) -> None:
    #    """ The Thread content to run on scheduler """
    #    print("Data Caching Schedule handling has been started!")
    #    print()
    #    try:
    #        while not self.terminating:
    #            schedule.run_pending()
    #            time.sleep(1)
    #    except Exception as e:
    #        print("Exception was detected", e)
    #        self.terminating = True
    #
    #    print()
    #    print("Schedule handling is terminating!")


# class Initializer(CoreInitialization):
#    def __init__(self, loop=None):
#        self.loop = loop or asyncio.get_event_loop()
#        super(Initializer, self).__init__()
#
#    def db_migration(self) -> None:
#        self.loop.run_until_complete(self.init_connection())

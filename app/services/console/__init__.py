from argparse import ArgumentParser

from pyfiglet import Figlet

from app.services.info import Info
from app.settings import Settings


class Console:
    def __init__(self) -> None:
        pass

    @classmethod
    def create_parser(cls) -> None:
        name = Info.get_name()
        description = Info.get_description()

        parser = ArgumentParser(
            description=name + " : " + description,
        )
        parser.add_argument(
            "--host",
            dest="host",
            type=str,
            default="127.0.0.1",
            help="The host " + name + " will listen to (default: 127.0.0.1)",
        )
        parser.add_argument(
            "--port",
            dest="port",
            type=int,
            default=8080,
            help="The port " + name + " will listen to (default: 8080)",
        )
        parser.add_argument(
            "--debug",
            dest="debug_mode",
            default=False,
            help="Start the application in debug mode",
            action="store_true",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            dest="quiet_mode",
            default=False,
            help="""Start the application in quiet mode (without banner, copyright)""",
            action="store_true",
        )
        parser.add_argument(
            "-v",
            "--version",
            dest="show_version",
            default=False,
            help="Show the application version",
            action="store_true",
        )

        return parser

    @classmethod
    def show_banner(cls, add_padding: bool = False) -> None:
        """ Show banner for XenXenXenSe Project """

        figlet = Figlet()

        print(figlet.renderText(Info.get_name()))
        print(Info.get_name() + " - " + "v." + Info.get_version())
        print(Info.get_description())
        print()
        print("Copyright (c) Stella IT.")
        print("This software is distributed under MIT License.")

        if add_padding:
            print()

    @staticmethod
    def print_xen_hostnames(show_title: bool = False) -> None:
        """ Print Xen Hostnames to screen """
        if show_title:
            print("Detected Clusters")

        for clusters in Settings.get_xen_clusters():
            print("*", clusters)
        
        print()

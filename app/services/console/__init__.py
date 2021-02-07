from pyfiglet import Figlet

from app.settings import Settings


class Console:
    def __init__(self) -> None:
        pass

    @classmethod
    def show_banner(cls, add_padding: bool = False) -> None:
        """ Show banner for XenXenXenSe Project """

        figlet = Figlet()

        print(figlet.renderText("XenXenXenSe"))
        print(
            "XenXenXenSe : An easy-to-use HTTP API of XenAPI for Web Application Developers"
        )
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

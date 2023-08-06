# -*- coding: utf-8 -*-
"""Zeroconf broadcast system."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv2"

import socket
from threading import Event, Thread

import zeroconf

from . import __version__


class ServiceShoutout(Thread):

    def __init__(self):
        """Init ServiceShoutout class."""
        super().__init__()

        # Class variables
        self.__checkdelay = 1
        self.__evt_exit = Event()

    def run(self):
        """Thread mainloop."""
        desc = {
            "version": __version__,
        }

        host_fqdn = socket.gethostname()
        host_name = host_fqdn.split(".")[0]
        host_ip4 = socket.gethostbyname(host_fqdn)

        zc_service_4 = zeroconf.ServiceInfo(
            "_revpipyload._tcp.local.",
            "{0}._revpipyload._tcp.local.".format(host_name),
            address=socket.inet_aton(host_ip4),
            port=55123,
            properties=desc,
        )

        zc_base = zeroconf.Zeroconf()
        zc_base.register_service(
            zc_service_4,
            allow_name_change=True,
        )
        while not self.__evt_exit.is_set():
            # TODO: Loopwork
            self.__evt_exit.wait(self.__checkdelay)

        zc_base.unregister_service(zc_service_4)
        zc_base.close()

    def stop(self):
        """Stop the thread mainloop."""
        self.__evt_exit.set()


if __name__ == '__main__':
    import signal

    root = ServiceShoutout()

    signal.signal(signal.SIGINT, lambda n, f: root.stop())
    signal.signal(signal.SIGTERM, lambda n, f: root.stop())

    root.start()
    root.join()

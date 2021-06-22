# Copyright (C) 2016-2017 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import logging

from lib.api.process import subprocess_checkcall
from lib.common.abstracts import Auxiliary
from lib.common.exceptions import CuckooError
from lib.core.driver import Driver
from lib.core.ioctl import driver_name as random_name

log = logging.getLogger(__name__)

class LoadZer0m0n(Auxiliary):
    """
    Load the zer0m0n kernel driver.
    它会在恶意软件执行过程中执行内核分析。恶意软件作者有很多方法可以绕过布谷鸟检测，他可以检测钩子，硬编码Nt*函数来避免钩子，检测虚拟机。。。
    这个驱动程序的目标是为用户提供一种可能性，让用户在经典的用户区分析和内核分析之间进行选择，难检测或绕过。
    """

    def start(self):
        if self.options.get("analysis") not in ("both", "kernel"):
            return

        try:
            d = Driver("zer0m0n", random_name)
        except CuckooError as e:
            log.error("Driver issue: %s", e)
            return

        # Disable the Program Compability Assistant (which would otherwise
        # show an annoying popup about our kernel driver not being signed).
        subprocess_checkcall(["sc", "stop", "PcaSvc"])

        try:
            d.install()
            log.info("Successfully loaded the zer0m0n kernel driver.")
        except CuckooError as e:
            log.error("Error loading zer0m0n: %s", e)

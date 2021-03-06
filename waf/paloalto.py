#!/usr/bin/env python2
# coding=utf-8

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import re

from lib.core.settings import WAF_ATTACK_VECTORS

__product__ = "Palo Alto Firewall (Palo Alto Networks)"


def detect(get_page):
    retval = False

    for vector in WAF_ATTACK_VECTORS:
        page, _, _ = get_page(get=vector)
        retval |= re.search(r"has been blocked in accordance with company policy", page or "", re.I) is not None
        retval |= all(_ in (page or "") for _ in ("Palo Alto Next Generation Security Platform", "Download Blocked"))
        if retval:
            break

    return retval

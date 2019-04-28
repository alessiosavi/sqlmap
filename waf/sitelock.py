#!/usr/bin/env python2
# coding=utf-8

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.settings import WAF_ATTACK_VECTORS

__product__ = "TrueShield Web Application Firewall (SiteLock)"


# Note: https://www.whitefirdesign.com/blog/2016/11/08/more-evidence-that-sitelocks-trueshield-web-application-firewall-is-really-incapsulas-waf/
def detect(get_page):
    retval = False

    for vector in WAF_ATTACK_VECTORS:
        page, _, _ = get_page(get=vector)
        retval |= any(_ in (page or "") for _ in ("SiteLock Incident ID", '<span class="value INCIDENT_ID">'))
        if retval:
            break

    return retval

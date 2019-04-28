#!/usr/bin/env python2

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from plugins.generic.enumeration import Enumeration as GenericEnumeration
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
from lib.core.data import queries
from lib.core.common import unArrayizeValue
from lib.core.enums import DBMS
from lib.core.settings import H2_DEFAULT_SCHEMA
from lib.request import inject


class Enumeration(GenericEnumeration):
    def getBanner(self):
        if not conf.getBanner:
            return

        if kb.data.banner is None:
            infoMsg = "fetching banner"
            logger.info(infoMsg)

            query = queries[DBMS.H2].banner.query
            kb.data.banner = unArrayizeValue(inject.getValue(query, safeCharEncode=True))

        return kb.data.banner

    def getPrivileges(self, *args):
        warnMsg = "on H2 it is not possible to enumerate the user privileges"
        logger.warn(warnMsg)

        return {}

    def getHostname(self):
        warnMsg = "on H2 it is not possible to enumerate the hostname"
        logger.warn(warnMsg)

    def getCurrentDb(self):
        return H2_DEFAULT_SCHEMA

    def getPasswordHashes(self):
        warnMsg = "on H2 it is not possible to list password hashes"
        logger.warn(warnMsg)

        return {}

#!/usr/bin/env python2
# coding=utf-8

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import binascii

from lib.core.common import getBytes
from lib.core.common import isDBMSVersionAtLeast
from plugins.generic.syntax import Syntax as GenericSyntax


class Syntax(GenericSyntax):
    @staticmethod
    def escape(expression, quote=True):
        """
        >>> from lib.core.common import Backend
        >>> Backend.setVersion('2')
        ['2']
        >>> Syntax.escape()
        "SELECT 'abcdefgh' FROM foobar"
        >>> Backend.setVersion('3')
        ['3']
        >>> Syntax.escape()
        "SELECT CAST(X'6162636465666768' AS TEXT) FROM foobar"
        """

        def escaper(value):
            # Reference: http://stackoverflow.com/questions/3444335/how-do-i-quote-a-utf-8-string-literal-in-sqlite3
            return "CAST(X'%s' AS TEXT)" % binascii.hexlify(getBytes(value))

        retVal = expression

        if isDBMSVersionAtLeast('3'):
            retVal = Syntax._escape(expression, quote, escaper)

        return retVal

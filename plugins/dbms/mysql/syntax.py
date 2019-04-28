#!/usr/bin/env python2
# coding=utf-8

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import binascii

from lib.core.convert import utf8encode
from plugins.generic.syntax import Syntax as GenericSyntax


class Syntax(GenericSyntax):
    @staticmethod
    def escape(expression, quote=True):
        """
        >>> Syntax.escape()
        'SELECT 0x6162636465666768 FROM foobar'
        """

        def escaper(value):
            retVal = None
            try:
                retVal = "0x%s" % binascii.hexlify(value)
            except UnicodeEncodeError:
                retVal = "CONVERT(0x%s USING utf8)" % "".join("%.2x" % ord(_) for _ in utf8encode(value))
            return retVal

        return Syntax._escape(expression, quote, escaper)

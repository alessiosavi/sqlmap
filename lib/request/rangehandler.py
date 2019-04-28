#!/usr/bin/env python2
# coding=utf-8

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.exception import SqlmapConnectionException
from thirdparty.six.moves import urllib as _urllib


class HTTPRangeHandler(_urllib.request.BaseHandler):
    """
    Handler that enables HTTP Range headers.

    Reference: http://stackoverflow.com/questions/1971240/python-seek-on-remote-file
    """

    @staticmethod
    def http_error_206(req, fp, code, msg, hdrs):
        # 206 Partial Content Response
        r = _urllib.response.addinfourl(fp, hdrs, req.get_full_url())
        r.code = code
        r.msg = msg
        return r

    @staticmethod
    def http_error_416(req, fp, code, msg, hdrs):
        # HTTP's Range Not Satisfiable error
        errMsg = "Invalid range"
        raise SqlmapConnectionException(errMsg)

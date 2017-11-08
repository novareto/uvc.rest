# -*- coding: utf-8 -*-

import json
from functools import wraps
from zope.security.management import checkPermission
from zope.security.interfaces import Unauthorized, Forbidden
from zope.authentication.interfaces import IUnauthenticatedPrincipal


def json_output(pretty_print=False, output_charset='utf-8'):
    def json_encoded(method):
        @wraps(method)
        def __call__(node, request):
            result = method(node, request)
            return json.dumps(
                result,
                encoding=output_charset,
                indent=pretty_print and 4 or None,
                sort_keys=pretty_print,
            )
        return __call__
    return json_encoded


def secure(permission):
    def secured_method(method):
        @wraps(method)
        def __call__(node, request):
            if not checkPermission(permission, node.context):
                # You are not allowed here.
                if IUnauthenticatedPrincipal.providedBy(request.principal):
                    raise Unauthorized
                raise Forbidden
            return method(node, request)
        return __call__
    return secured_method


def content_type(ct):
    def typed_response(method):
        @wraps(method)
        def __call__(node, request):
            request.response.setHeader("Content-type", ct)
            return method(node, request)
        return __call__
    return typed_response

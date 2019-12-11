# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import json
import grokcore.component as grok

from grokcore.site import Application
from uvc.rest.components import IRESTNode, RESTAdapter, ICORS
from uvc.rest.components import http_method_resolve
from uvc.rest.service import Endpoint, EndpointsDispatcher
from zope.interface import Interface, implementer, provider


def http_method_resolve(inst, request):
    httpmethod = request.method.upper()
    method = getattr(inst, httpmethod, None)
    if method is not None:
        return method
    raise NotImplementedError("`%s` method has no bound resolver." % httpmethod)


class IFoo(Interface):
    pass


class MyApp(Application):
    pass


class NoCorsApp(Application):
    pass


class Dump(Endpoint):

    __resolve__ = http_method_resolve

    def GET(self, request):
        return json.dumps({"SomeKey": "SomeValue"})


def remover(context):
    @provider(IRESTNode)
    def do_delete(request):
        return "DELETED !!"

    return do_delete


class JSON(EndpointsDispatcher):
    grok.name("json")

    endpoints = {"dump": Dump, "delete": remover}


class RestService(RESTAdapter):
    grok.context(MyApp)
    grok.name("service")

    __resolve__ = http_method_resolve

    def GET(self, request):
        return "HI FROM GET"


@implementer(ICORS)
class AllowAll(grok.Adapter):
    """Very generic CORS allowance. Works site-wide
    """

    grok.context(MyApp)

    def OPTIONS(self, request):
        request.response.setHeader("Access-Control-Allow-Methods", "PUT")
        request.response.setHeader(
            "Access-Control-Allow-Origin", "http://localhost:8080"
        )
        return b""

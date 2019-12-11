# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import grok

from uvc.rest.decorators import secure
from uvc.rest.components import RESTAdapter, ICORS
from zope.interface import implementer
from zope.pluggableauth import PluggableAuthentication
from zope.authentication.interfaces import IAuthentication
from gocept.webtoken import CryptographicKeys, ICryptographicKeys
import pkg_resources


class MyAuthApp(grok.Application, grok.Container):
    def setup_pau(PAU):
        PAU.authenticatorPlugins = ("auth.bearer",)
        PAU.credentialsPlugins = (
            "creds.bearer",
            "Zope Realm Basic-Auth",
            "No Challenge if Authenticated",
        )

    grok.local_utility(
        PluggableAuthentication, IAuthentication, public=True, setup=setup_pau
    )


crypto_keys = CryptographicKeys(
    pkg_resources.resource_filename("uvc.rest", "tests/fixtures/keys"), ["novareto", ]
)

grok.global_utility(crypto_keys, direct=True)


def http_method_resolve(inst, request):
    httpmethod = request.method.upper()
    method = getattr(inst, httpmethod, None)
    if method is not None:
        return method
    raise NotImplementedError("`%s` method has no bound resolver." % httpmethod)


class RestService(RESTAdapter):
    grok.context(MyAuthApp)
    grok.name("service")

    __resolve__ = http_method_resolve

    @secure("zope.View")
    def GET(self, request):
        return "HI FROM GET"


@implementer(ICORS)
class AllowAll(grok.Adapter):
    """Very generic CORS allowance. Works site-wide
    """

    grok.context(MyAuthApp)

    def OPTIONS(self, request):
        request.response.setHeader("Access-Control-Allow-Methods", "PUT")
        request.response.setHeader(
            "Access-Control-Allow-Origin", "http://localhost:8080"
        )
        return b""

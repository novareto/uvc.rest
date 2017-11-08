"""
BASIC REST
----------

  >>> root = getRootFolder()
  >>> root['app'] = MyApp()
  >>> root['nocorsapp'] = NoCorsApp()

  >>> response = http_call('OPTIONS', 'http://localhost/app')
  >>> response.getHeaders()
  [('Access-Control-Allow-Methods', 'PUT'), ('Access-Control-Allow-Origin', 'http://localhost:8080'), ('Content-Length', '0')]

  >>> response = http_call('OPTIONS', 'http://localhost/nocorsapp')
  Traceback (most recent call last):
  ...
  Unauthorized

  >>> response = http_call('GET', 'http://localhost/app')
  >>> print response.getBody()
  HI FROM GET

  >>> response = http_call('POST', 'http://locahost/app')
  Traceback (most recent call last):
  ...
  NotImplementedError: `POST` method has no bound resolver.

SERVICES
--------

"""


import grokcore.component as grok

from grokcore import content
from uvc.rest.components import RESTNode, ICORS
from zope.interface import Interface, implementer


class IFoo(Interface):
    pass


class MyApp(content.Container):
    pass


class NoCorsApp(content.Container):
    pass


class RestServie(RESTNode):
    grok.context(MyApp)
    grok.name('service')

    def __resolve__(self, request):
        httpmethod = request.method.upper()
        method = getattr(self, httpmethod, None)
        if method is not None:
            return method
        raise NotImplementedError(
                "`%s` method has no bound resolver." % httpmethod)

    def GET(self, request):
        return "HI FROM GET"


@implementer(ICORS)
class AllowAll(grok.Adapter):
    """Very generic CORS allowance. Works site-wide
    """
    grok.context(MyApp)

    def OPTIONS(self, request):
        request.response.setHeader(
            'Access-Control-Allow-Methods', 'PUT')
        request.response.setHeader(
                'Access-Control-Allow-Origin', 'http://localhost:8080')
        return

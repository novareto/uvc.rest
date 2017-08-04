"""
  >>> root = getRootFolder()
  >>> root['app'] = MyApp()

  >>> response = http_call('GET', 'http://localhost/++rest++a/app/service')
  >>> print response.getBody()
  GET
"""



import grokcore.component as grok
from grokcore import rest, view, security, content
from zope.interface import Interface
from uvc.rest import RESTService

class IFoo(Interface):
    pass

class MyApp(content.Container):
    pass

class LayerA(rest.IRESTLayer):
    rest.restskin('a')


class RestServie(RESTService):
    grok.context(MyApp)
    grok.name('service')
    view.layer(LayerA)

    def GET(self):
        return "HI FROM GET"

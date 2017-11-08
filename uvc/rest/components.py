# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface, implementer


class ICORS(Interface):

    def OPTIONS(request):
        """Expose the CORS policy of the context.
        """


class IRESTNode(Interface):

    def __call__(request):
        """Returns a publishable result.
        """

@implementer(IRESTNode)
class RESTNode(object):

    def __init__(self, context):
        self.context = context
    
    def __resolve__(self, request):
        raise NotImplementedError('Code your own.')

    def __call__(self, request):
        method = self.__resolve__(request)
        return method(request)


class RESTAdapter(RESTNode, grok.Adapter):
    grok.baseclass()
    grok.context(Interface)


def http_method_resolve(inst, request):
    httpmethod = request.method.upper()
    method = getattr(inst, httpmethod, None)
    if method is not None:
        return method
    raise NotImplementedError(
        "`%s` method has no bound resolver." % httpmethod)

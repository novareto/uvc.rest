# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface, implementer


class ICORS(Interface):

    def OPTIONS(request):
        """Expose the CORS policy of the context.
        """


class IRESTNode(Interface):

    def publish(request):
        """Returns a publishable result.
        """


@implementer(IRESTNode)
class RESTNode(grok.Adapter):
    grok.baseclass()
    grok.context(Interface)

    def __resolve__(self, request):
        raise NotImplementedError('Code your own.')

    def publish(self, request):
        method = self.__resolve__(request)
        return method(request)

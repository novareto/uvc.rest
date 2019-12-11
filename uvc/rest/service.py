# -*- coding: utf-8 -*-

import grok

from .components import RESTNode
from grokcore.site import IApplication
from zope.component import queryMultiAdapter
from zope.interface import Interface, Attribute, implementer
from zope.location import LocationProxy
from zope.publisher.browser import applySkin
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.browser import IBrowserPublisher


class IServicePublication(Interface):
    pass


class IService(Interface):
    layer = Attribute("Dedicated skin layer")


@implementer(IBrowserPublisher)
class Endpoint(RESTNode):
    """RestNode that are published through a normal traversing process.
    It is usually used as Service actions. See `EndpointsDispatcher` in
    this module.
    """

    def browserDefault(self, request):
        return self, None


class Service(grok.MultiAdapter):
    grok.baseclass()
    grok.adapts(IApplication, IHTTPRequest)
    grok.implements(IPublishTraverse, IService)
    grok.provides(IService)

    layer = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        raise NotImplementedError("implement me")


class EndpointsDispatcher(Service):
    grok.baseclass()

    endpoints = {}

    def publishTraverse(self, request, name):
        endpoint = self.endpoints.get(name, None)
        if endpoint is not None:
            return endpoint(self.context)


class ServicesNamespace(grok.MultiAdapter):
    grok.name("services")
    grok.provides(ITraversable)
    grok.adapts(IApplication, IHTTPRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        if not name:
            raise NotImplementedError("Please specify a service.")

        service = queryMultiAdapter((self.context, self.request), IService, name=name)

        if service is None:
            raise LookupError("Unknown service : %s" % name)
        else:
            if service.layer is not None:
                applySkin(self.request, service.layer)
            return LocationProxy(service, self.context, "++services++%s" % name)

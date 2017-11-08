# -*- coding: utf-8 -*-

import grok

from zope.component import getMultiAdapter
from zope.interface import Interface, Attribute, implementer
from zope.location import LocationProxy
from zope.publisher.browser import applySkin
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable


class IServicePublication(Interface):
    pass


class IService(Interface):
    layer = Attribute('Dedicated skin layer')


class Service(grok.MultiAdapter):
    grok.baseclass()
#    grok.adapts(uvcsite.IUVCSite, IHTTPRequest)
    grok.implements(IPublishTraverse, IService)
    grok.provides(IService)

    layer = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        raise NotImplementedError('implement me')


class ServicesNamespace(grok.MultiAdapter):
    grok.baseclass()
    grok.name('services')
    grok.provides(ITraversable)
#    grok.adapts(uvcsite.IUVCSite, IHTTPRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        if not name:
            raise NotImplementedError('Please specify a service.')

        service = getMultiAdapter(
            (self.context, self.request), IService, name=name)
        if service.layer is not None:
            applySkin(self.request, service.layer)
        print "Accessing Service %s" % service
        return LocationProxy(service, self.context, "++services++%s" % name)

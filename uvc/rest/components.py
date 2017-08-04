# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import zope.location

from zope import interface
from grokcore.view import ViewSupport
from grokcore.rest.interfaces import IREST
from grokcore.component.interfaces import IContext


class IRESTService(IREST):
    pass


class RESTService(zope.location.Location, ViewSupport):
    """Base class for REST views in Grok applications."""
    interface.implements(IRESTService, IContext)

    def __init__(self, context, request):
        self.context = self.__parent__ = context
        self.request = request

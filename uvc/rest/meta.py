# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de


from martian.error import GrokError
from zope import interface, component
from grokcore.view import make_checker
from zope.interface.interface import InterfaceClass

import martian

import grokcore.component
import grokcore.view
import grokcore.security
from .components import RESTService
from zope import interface
from martian import util


def default_view_name(component, module=None, **data):
    return component.__name__.lower()


METHODS = ('GET', 'POST', 'PUT')


class RESTServiceGrokker(martian.ClassGrokker):
    """Grokker for methods of a `grok.REST` subclass.
    """
    martian.component(RESTService)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=grokcore.rest.IRESTLayer)
    martian.directive(grokcore.security.require, name='permission')
    martian.directive(grokcore.component.name, get_default=default_view_name)
    martian.directive(grokcore.component.provides, default=interface.Interface)

    def execute(self, factory, config, permission, context, provides,
                layer, name, **kw):
        factory.__view_name__ = name
        adapts = (context, layer)

        config.action(
            discriminator=('adapter', adapts, provides, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, adapts, provides, name),
            )


        def register(method):
            method_view = type(
                factory.__name__, (factory,),
                {'__call__': method})

            adapts = (context, layer)
            print adapts
            adapts = (factory, layer)
            print adapts
            config.action(
                discriminator=('adapter', adapts, interface.Interface, name),
                callable=grokcore.component.provideAdapter,
                args=(method_view, adapts, interface.Interface, name),
                )
            config.action(
                discriminator=('protectName', method_view, '__call__'),
                callable=make_checker,
                args=(factory, method_view, permission),
                )
        methods = util.methods_from_class(factory)

        for method in methods:
            name = method.__name__
            if name in METHODS:
                print "REGISTER", method
                register(method)
        return True

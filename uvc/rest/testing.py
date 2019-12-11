# -*- coding: utf-8 -*-

from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml


def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok("grokcore.component.meta", config)
    zcml.do_grok("grokcore.security.meta", config)
    zcml.do_grok("grokcore.view.meta", config)
    zcml.do_grok("uvc.rest.meta", config)
    zcml.do_grok(module_name, config)
    config.execute_actions()

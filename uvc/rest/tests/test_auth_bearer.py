# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import unittest
from uvc.rest.testing import test_rest_layer, http_call
import grokcore.site.util


class TestAPI(unittest.TestCase):
    layer = test_rest_layer

    def setUp(self):
        from zope.component.hooks import setSite
        from uvc.rest.tests.fixtures.auth_app import MyAuthApp

        root = self.layer.getRootFolder()
        grokcore.site.util.create_application(MyAuthApp, root, 'authapp')
        app = root['authapp']
        setSite(app)

    def test_with_cors(self):
        response = http_call("GET", "http://localhost/authapp", Authorization="Bearer blablub")
        print(response.getBody())

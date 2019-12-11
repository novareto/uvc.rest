# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import unittest
from uvc.rest.testing import test_rest_layer, http_call


class TestAPI(unittest.TestCase):
    layer = test_rest_layer

    def setUp(self):
        from uvc.rest.tests.fixtures.app import MyApp, NoCorsApp

        root = self.layer.getRootFolder()
        root["app"] = MyApp()
        root["no_cors_app"] = NoCorsApp()

    def test_with_cors(self):
        response = http_call("OPTIONS", "http://localhost/app")
        self.assertEqual(
            response.getHeaders(),
            [
                ("Access-Control-Allow-Methods", "PUT"),
                ("Access-Control-Allow-Origin", "http://localhost:8080"),
                ("Content-Length", "0"),
            ],
        )

    def test_without_cors(self):
        import zope.security.interfaces

        with self.assertRaises(zope.security.interfaces.Unauthorized):
            http_call("OPTIONS", "http://localhost/no_cors_app")

    def test_existing_get(self):
        self.assertEqual(
            http_call("GET", "http://localhost/app").getBody(), b"HI FROM GET"
        )

    def not_existing_post(self):
        with self.assertRaces(NotImplementedError):
            http_call('POST', 'http://locahost/app')

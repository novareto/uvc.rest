# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import json
import unittest
from uvc.rest.testing import test_rest_layer, http_call


class TestAPI(unittest.TestCase):
    layer = test_rest_layer

    def setUp(self):
        from uvc.rest.tests.fixtures.app import MyApp, NoCorsApp

        root = self.layer.getRootFolder()
        root["app"] = MyApp()
        root["no_cors_app"] = NoCorsApp()

    def test_not_implemnted_service(self):
        with self.assertRaises(NotImplementedError):
            http_call("OPTIONS", "http://localhost/app/++services++")

    def test_unknown_service(self):
        with self.assertRaises(LookupError):
            http_call("OPTIONS", "http://localhost/app/++services++test")

    def test_get_on_service(self):
        self.assertEqual(
            json.loads(http_call("GET", "http://localhost/app/++services++json/dump").getBody()),
            {"SomeKey": "SomeValue"},
        )

    def test_unauth(self):
        import zope.security.interfaces
        with self.assertRaises(zope.security.interfaces.Unauthorized):
            http_call("OPTIONS", "http://localhost/app/++services++json/dump")

    def test_delete_on_get(self):
        self.assertEqual(
            http_call("GET", "http://localhost/app/++services++json/delete").getBody(),
            b"DELETED !!",
        )

    def test_delete_on_put(self):
        self.assertEqual(
            http_call("PUT", "http://localhost/app/++services++json/delete").getBody(),
            b"DELETED !!",
        )

    def test_delete_on_delete(self):
        self.assertEqual(
            http_call(
                "DELETE", "http://localhost/app/++services++json/delete"
            ).getBody(),
            b"DELETED !!",
        )

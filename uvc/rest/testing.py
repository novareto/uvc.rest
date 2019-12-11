# -*- coding: utf-8 -*-


import uvc.rest
import zope.testbrowser.wsgi
import zope.app.wsgi.testlayer
import zope.testbrowser.wsgi


from six import StringIO
from webtest import TestRequest
from zope.app.wsgi.testlayer import NotInBrowserLayer, FakeResponse


def http(string, handle_errors=True):
    app = zope.testbrowser.wsgi.Layer.get_app()
    if app is None:
        raise NotInBrowserLayer(NotInBrowserLayer.__doc__)

    request = TestRequest.from_file(StringIO(string))
    request.environ["wsgi.handleErrors"] = handle_errors
    request.environ["HTTP_X_UVCSITE_REST"] = "service"
    response = request.get_response(app)
    return FakeResponse(response)


def http_call(method, path, data=None, **kw):
    """Function to help make RESTful calls.
    method - HTTP method to use
    path - testbrowser style path
    data - (body) data to submit
    kw - any request parameters
    """

    if path.startswith("http://localhost"):
        path = path[len("http://localhost") :]
    request_string = "%s %s HTTP/1.1\n" % (method, path)
    for key, value in kw.items():
        request_string += "%s: %s\n" % (key, value)
    if data is not None:
        request_string += "Content-Length:%s\n" % len(data)
        request_string += "\r\n"
        request_string += data
    return http(request_string, handle_errors=False)


class TestRestLayer(
    zope.testbrowser.wsgi.TestBrowserLayer, zope.app.wsgi.testlayer.BrowserLayer
):
    def get_browser(self, url, handle_errors=True):
        browser = zope.testbrowser.wsgi.Browser(url, wsgi_app=self.make_wsgi_app())
        browser.handleErrors = handle_errors
        return browser


test_rest_layer = TestRestLayer(uvc.rest)

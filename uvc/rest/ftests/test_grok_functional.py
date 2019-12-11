import re
import unittest, doctest
import uvc.rest

from pkg_resources import resource_listdir
from zope.testing import renormalizing
from zope.app.wsgi.testlayer import BrowserLayer
import zope.testbrowser.wsgi
from zope.app.wsgi.testlayer import NotInBrowserLayer, FakeResponse
from webtest import TestRequest
from six import StringIO


def http(string, handle_errors=True):
    app = zope.testbrowser.wsgi.Layer.get_app()
    if app is None:
        raise NotInBrowserLayer(NotInBrowserLayer.__doc__)

    request = TestRequest.from_file(StringIO(string))
    request.environ['wsgi.handleErrors'] = handle_errors
    request.environ['HTTP_X_UVCSITE_REST'] = 'service'
    response = request.get_response(app)
    return FakeResponse(response)



FunctionalLayer = BrowserLayer(uvc.rest)

checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])

def http_call(method, path, data=None, **kw):
    """Function to help make RESTful calls.
    method - HTTP method to use
    path - testbrowser style path
    data - (body) data to submit
    kw - any request parameters
    """

    if path.startswith('http://localhost'):
        path = path[len('http://localhost'):]
    request_string = '%s %s HTTP/1.1\n' % (method, path)
    for key, value in kw.items():
        request_string += '%s: %s\n' % (key, value)
    if data is not None:
        request_string += 'Content-Length:%s\n' % len(data)
        request_string += '\r\n'
        request_string += data
    return http(request_string, handle_errors=False)


def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'uvc.rest.ftests.%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            checker=checker,
            extraglobs=dict(http_call=http_call,
                            http=http,
                            getRootFolder=FunctionalLayer.getRootFolder),
            optionflags=(doctest.ELLIPSIS+
                         doctest.NORMALIZE_WHITESPACE+
                         doctest.REPORT_NDIFF))
        test.layer = FunctionalLayer

        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['rest']:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

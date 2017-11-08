# -*- coding: utf-8 -*-

from .components import IRESTNode, ICORS
from zope.app.publication.http import HTTPPublication
from zope.component import queryAdapter
from zope.security.interfaces import Unauthorized
from grokcore.view.publication import ZopePublicationSansProxy
from zope.app.publication.requestpublicationfactories import (
    HTTPFactory)


class RESTPublication(ZopePublicationSansProxy, HTTPPublication):

    def callObject(self, request, ob):

        if request.method == 'OPTIONS':
            # Our request is an OPTIONS request.
            # To statisfy the CORS requirements, we answer.
            # In order to keep this pluggable, we adapt the result
            # of the traversing instead of catching the request before
            # traversal.
            cors = ICORS(ob, None)
            if cors is None:
                # we don't have a CORS handler.
                # it means we don't even have a generic adapter.
                # Raise Unauthorized : CORS is not allowed.
                raise Unauthorized
            return cors.OPTIONS(request)
        elif IRESTNode.providedBy(ob):
            # The returned object is already a REST node
            return ob(request)
        else:
            # We make sure the
            name = request.environment['HTTP_X_UVCSITE_REST'].lower()
            restnode = queryAdapter(ob, IRESTNode, name=name)
            if restnode is None:
                raise NotImplementedError('No REST node %s' % name)
            return restnode(request)


class RESTFactory(HTTPFactory):

    def canHandle(self, environ):
        """Our REST factory only accepts requests with our custom header or
           the OPTIONS method.
        """
        return (
            'HTTP_X_UVCSITE_REST' in environ or
            environ['REQUEST_METHOD'] == 'OPTIONS')

    def __call__(self):
        request, publication = super(RESTFactory, self).__call__()
        return request, RESTPublication

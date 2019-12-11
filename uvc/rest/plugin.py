# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import grok
import json

from zope.component import getUtility
from gocept.webtoken import ICryptographicKeys
from gocept.webtoken import extract_token

from zope.pluggableauth.interfaces import (
    IPrincipalInfo,
    IAuthenticatorPlugin,
    ICredentialsPlugin,
)


class BearerTokenAuthCredentialsPlugin(grok.GlobalUtility):
    grok.name("creds.bearer")
    grok.implements(ICredentialsPlugin)

    @property
    def keys(self):
        return getUtility(ICryptographicKeys)

    def canHandle(self, environ):
        return (
            "HTTP_X_UVCSITE_REST" in environ or environ["REQUEST_METHOD"] == "OPTIONS"
        )

    def extractCredentials(self, request):
        if self.canHandle(request._environ):
            import pdb; pdb.set_trace()
            if request._auth:
                access_token = extract_token(request._auth)
                if access_token:
                    return {"access_token": access_token}
        return None

    def challenge(self, request):
        if self.canHandle(request._environ):
            request.response.setStatus(401)
            return True
        return False

    def logout(self, request):
        return False


class AccessTokenHolder(object):
    grok.implements(IPrincipalInfo)

    credentialsPlugin = None
    authenticatorPlugin = None

    def __repr__(self):
        return '<AccessTokenHolder "%s">' % self.id

    def __init__(self, token, infos):
        userid = infos["userid"]
        client = infos["client"]
        self.id = userid
        self.title = u"Access token %r for %r (%r)" % (token, userid, client)
        self.description = u"OAuth2 access token provided for %r (%r)" % (
            userid,
            client,
        )


class AuthenticateBearer(grok.GlobalUtility):
    grok.name("auth.bearer")
    grok.implements(IAuthenticatorPlugin)

    def verify(self, token):
        import pdb; pdb.set_trace()
        params = {"access_token": token}
        try:
            response = urllib2.urlopen(self.verify_token, urlencode(params))
            token = json.load(response)
            return token
        except HTTPError as he:
            return None
        except URLError as e:
            return None
        else:
            return None

    def authenticateCredentials(self, credentials):
        """Return principal info if credentials can be authenticated
        """
        import pdb; pdb.set_trace()
        if not isinstance(credentials, dict):
            return None

        access_token = credentials.get("access_token")
        if access_token is None:
            return None

        infos = self.verify(access_token)
        if infos is not None:
            return AccessTokenHolder(access_token, infos)
        return None

    def principalInfo(self, id):
        return None

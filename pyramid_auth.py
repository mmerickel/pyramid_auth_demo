import cryptacular.bcrypt

from pyramid.authentication import AuthTktCookieHelper
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.exceptions import Forbidden
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Authenticated, Everyone
from pyramid.security import Allow, Deny, ALL_PERMISSIONS, DENY_ALL
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.url import route_url
from pyramid.view import view_config

from zope.interface import implements

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

# for example purposes only
USERS = {
    'luser': crypt.encode('luser'),
    'admin': crypt.encode('admin'),
}

GROUPS = {
    'admin': [ 'admin' ],
}

class MyAuthenticationPolicy(object):
    implements(IAuthenticationPolicy)

    def __init__(self, settings):
        self.cookie = AuthTktCookieHelper(settings['auth.secret'])

    def remember(self, request, principal, **kw):
        return self.cookie.remember(request, principal, **kw)

    def forget(self, request):
        return self.cookie.forget(request)

    def unauthenticated_userid(self, request):
        result = self.cookie.identify(request)
        if result:
            return result['userid']

    def authenticated_userid(self, request):
        uid = self.unauthenticated_userid(request)
        # check that the user actually exists
        if uid in USERS:
            return uid

    def effective_principals(self, request):
        principals = [Everyone]
        uid = self.authenticated_userid(request)
        if uid:
            principals += [Authenticated, 'u:%s' % uid]
            principals.extend(('g:%s' % g for g in GROUPS.get(uid, [])))
        return principals

class Root(dict):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request
        self['users'] = UserContainer(self, 'users')

class UserContainer(object):
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name

    def __getitem__(self, key):
        if key in USERS:
            u = User(key)
            u.__parent__ = self
            u.__name__ = key
            return u
        raise KeyError

class User(object):
    @property
    def __acl__(self):
        return [
            (Allow, 'u:%s' % self.login, ('view', 'edit')),
        ]

    def __init__(self, login):
        self.login = login

@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    return {
        'user': authenticated_userid(request),
    }

@view_config(context=Forbidden)
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return Forbidden()

    loc = route_url('login', request, _query=(('next', request.path),))
    return HTTPFound(location=loc)

@view_config(route_name='login', renderer='login.mako')
def login_view(request):
    next = request.params.get('next') or route_url('home', request)
    login = ''
    did_fail = False
    if 'submit' in request.POST:
        login = request.POST.get('login', '')
        passwd = request.POST.get('passwd', '')

        hashed_passwd = USERS.get(login, '')
        if crypt.check(hashed_passwd, passwd):
            headers = remember(request, login)
            return HTTPFound(location=next, headers=headers)
        did_fail = True

    return {
        'login': login,
        'next': next,
        'failed_attempt': did_fail,
    }

@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    loc = route_url('home', request)
    return HTTPFound(location=loc, headers=headers)

@view_config(route_name='user', permission='view', renderer='user.mako')
def user_view(request):
    user = request.context
    #login = request.matchdict['login']
    login = user.login

    return {
        'login': login,
        'groups': GROUPS.get(login, []),
    }

@view_config(route_name='users', permission='view', renderer='users.mako')
def users_view(request):
    return {
        'users': sorted(USERS.keys()),
    }

def main(global_settings, **settings):
    authn_policy = MyAuthenticationPolicy(settings)
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        root_factory=Root,
    )

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('users', '/users', traverse='/users')
    config.add_route('user', '/users/{login}', traverse='/users/{login}')

    config.scan(__name__)
    return config.make_wsgi_app()

if __name__ == '__main__':
    settings = {
        'auth.secret': 'seekrit',
        'mako.directories': '%s:templates' % __name__,
    }
    app = main({}, **settings)

    from paste.httpserver import serve
    serve(app, host='0.0.0.0', port='5000')

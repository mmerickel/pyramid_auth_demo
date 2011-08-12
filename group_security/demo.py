from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import Authenticated
from pyramid.security import Allow, ALL_PERMISSIONS
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.url import route_url
from pyramid.view import view_config

# for example purposes only
USERS = {
    'luser': 'luser',
    'admin': 'admin',
}

GROUPS = {
    'admin': [ 'admin' ],
}

def groupfinder(userid, request):
    if userid in USERS:
        return ['g:%s' % g for g in GROUPS.get(userid, [])]

class Root(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, Authenticated, 'view'),
    ]

    def __init__(self, request):
        self.request = request

@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    return {
        'user': authenticated_userid(request),
    }

@view_config(context=HTTPForbidden)
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

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

        if passwd == USERS.get(login, None):
            headers = remember(request, login)
            return HTTPFound(location=next, headers=headers)
        did_fail = True

    return {
        'login': login,
        'next': next,
        'failed_attempt': did_fail,
        'users': USERS,
    }

@view_config(route_name='logout')
def logout_view(request):
    headers = forget(request)
    loc = route_url('home', request)
    return HTTPFound(location=loc, headers=headers)

@view_config(route_name='secure', permission='view', renderer='secure.mako')
def secure_view(request):
    login = authenticated_userid(request)

    return {
        'user': login,
        'groups': GROUPS.get(login, []),
    }

@view_config(route_name='admin', permission='admin', renderer='admin.mako')
def admin_view(request):
    return {
        'users': USERS,
    }

def main(global_settings, **settings):
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        callback=groupfinder
    )
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
    config.add_route('secure', '/secure')
    config.add_route('admin', '/secure/admin')

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

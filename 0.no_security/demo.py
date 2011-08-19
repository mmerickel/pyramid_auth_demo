import urllib

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import view_config

### DEFINE MODEL
class User(object):
    def __init__(self, login, password, groups=[]):
        self.login = login
        self.password = password
        self.groups = groups

    def check_password(self, passwd):
        return self.password == passwd

class Page(object):
    def __init__(self, title, uri, body, owner):
        self.title = title
        self.uri = uri
        self.body = body
        self.owner = owner

def websafe_uri(txt):
    uri = txt.replace(' ', '-')
    return urllib.quote(uri)

### INITIALIZE MODEL
USERS = {}
PAGES = {}

def _make_demo_user(login, **kw):
    kw.setdefault('password', login)
    USERS[login] = User(login, **kw)

_make_demo_user('luser')
_make_demo_user('editor', groups=['editors'])
_make_demo_user('admin', groups=['admin'])

def _make_demo_page(title, **kw):
    uri = kw.setdefault('uri', websafe_uri(title))
    PAGES[uri] = Page(title, **kw)

_make_demo_page('hello', owner='luser', body='<h1>Hello World!</h2>')

### DEFINE VIEWS
@view_config(route_name='home', renderer='home.mako')
def home_view(request):
    login = authenticated_userid(request)
    user = USERS.get(login)

    return {
        'user': user,
        'user_pages': [p for (t, p) in PAGES.iteritems() if p.owner == login],
    }

@view_config(route_name='login', renderer='login.mako')
def login_view(request):
    next = request.params.get('next') or request.route_url('home')
    login = ''
    did_fail = False
    if 'submit' in request.POST:
        login = request.POST.get('login', '')
        passwd = request.POST.get('passwd', '')

        user = USERS.get(login, None)
        if user and user.check_password(passwd):
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
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)

@view_config(route_name='users',  renderer='users.mako')
def users_view(request):
    return {
        'users': sorted(USERS.keys()),
    }

@view_config(route_name='user', renderer='user.mako')
def user_view(request):
    login = request.matchdict['login']
    user = USERS[login]
    pages = [p for (t, p) in PAGES.iteritems() if p.owner == login]

    return {
        'user': user,
        'pages': pages,
    }

@view_config(route_name='pages', renderer='pages.mako')
def pages_view(request):
    return {
        'pages': PAGES.values(),
    }

@view_config(route_name='page', renderer='page.mako')
def page_view(request):
    uri = request.matchdict['title']
    page = PAGES[uri]

    return {
        'title': page.title,
        'owner': page.owner,
        'body': page.body,
    }

@view_config(route_name='create_page', renderer='create_page.mako')
def create_page_view(request):
    uri = request.matchdict['title']
    page = PAGES[uri]

    return {
        'title': page.title,
        'owner': page.owner,
        'body': page.body,
    }

### CONFIGURE PYRAMID
def main(global_settings, **settings):
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
    )
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
    )

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('users', '/users')
    config.add_route('user', '/users/{login}')

    config.add_route('pages', '/pages')
    config.add_route('create_page', '/create_page')
    config.add_route('page', '/pages/{title}')
    config.add_route('edit_page', '/pages/{title}/edit')

    config.scan(__name__)
    return config.make_wsgi_app()

### SIMPLE STARTUP
if __name__ == '__main__':
    settings = {
        'auth.secret': 'seekrit',
        'mako.directories': '%s:templates' % __name__,
    }
    app = main({}, **settings)

    from paste.httpserver import serve
    serve(app, host='0.0.0.0', port='5000')

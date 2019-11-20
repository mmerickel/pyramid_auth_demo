import urllib.parse

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import forbidden_view_config
from pyramid.view import view_config

### DEFINE MODEL
class User(object):
    def __init__(self, login, password, groups=None):
        self.login = login
        self.password = password
        self.groups = groups or []

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
    return urllib.parse.quote(uri)

### INITIALIZE MODEL
USERS = {}
PAGES = {}

def _make_demo_user(login, **kw):
    kw.setdefault('password', login)
    USERS[login] = User(login, **kw)
    return USERS[login]

_make_demo_user('luser')
_make_demo_user('editor', groups=['editor'])
_make_demo_user('admin', groups=['admin'])

def _make_demo_page(title, **kw):
    uri = kw.setdefault('uri', websafe_uri(title))
    PAGES[uri] = Page(title, **kw)
    return PAGES[uri]

_make_demo_page('hello', owner='luser',
                body='''
<h3>Hello World!</h3><p>I'm the body text</p>''')

### MAP GROUPS TO PERMISSIONS
class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'create'),
        (Allow, 'g:editor', 'edit'),
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

def groupfinder(userid, request):
    user = USERS.get(userid)
    if user:
        return ['g:%s' % g for g in user.groups]

### DEFINE VIEWS
@forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if request.authenticated_userid is not None:
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)

@view_config(
    route_name='home',
    renderer='home.mako',
)
def home_view(request):
    login = request.authenticated_userid
    user = USERS.get(login)

    return {
        'user': user,
        'user_pages': [p for (t, p) in PAGES.items() if p.owner == login],
    }

@view_config(
    route_name='login',
    renderer='login.mako',
)
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

@view_config(
    route_name='logout',
)
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)

@view_config(
    route_name='users',
    permission='admin',
    renderer='users.mako',
)
def users_view(request):
    return {
        'users': sorted(USERS.keys()),
    }

@view_config(
    route_name='user',
    permission='admin',
    renderer='user.mako',
)
def user_view(request):
    login = request.matchdict['login']
    user = USERS.get(login)
    if not user:
        raise HTTPNotFound()

    pages = [p for (t, p) in PAGES.items() if p.owner == login]

    return {
        'user': user,
        'pages': pages,
    }

@view_config(
    route_name='pages',
    renderer='pages.mako',
)
def pages_view(request):
    return {
        'pages': PAGES.values(),
    }

@view_config(
    route_name='page',
    renderer='page.mako',
)
def page_view(request):
    uri = request.matchdict['title']
    page = PAGES.get(uri)
    if not page:
        raise HTTPNotFound()

    return {
        'page': page,
    }

def validate_page(title, body):
    errors = []

    title = title.strip()
    if not title:
        errors.append('Title may not be empty')
    elif len(title) > 32:
        errors.append('Title may not be longer than 32 characters')

    body = body.strip()
    if not body:
        errors.append('Body may not be empty')

    return {
        'title': title,
        'body': body,
        'errors': errors,
    }

@view_config(
    route_name='create_page',
    permission='create',
    renderer='edit_page.mako',
)
def create_page_view(request):
    owner = request.authenticated_userid

    errors = []
    body = title = ''
    if request.method == 'POST':
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')

        v = validate_page(title, body)
        title = v['title']
        body = v['body']
        errors += v['errors']

        if not errors:
            page = _make_demo_page(title, owner=owner, body=body)
            url = request.route_url('page', title=page.uri)
            return HTTPFound(location=url)

    return {
        'title': title,
        'owner': owner,
        'body': body,
        'errors': errors,
    }

@view_config(
    route_name='edit_page',
    permission='edit',
    renderer='edit_page.mako',
)
def edit_page_view(request):
    uri = request.matchdict['title']
    page = PAGES.get(uri)
    if not page:
        raise HTTPNotFound()

    errors = []
    title = page.title
    body = page.body
    if request.method == 'POST':
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')

        v = validate_page(title, body)
        title = v['title']
        body = v['body']
        errors += v['errors']

        if not errors:
            del PAGES[uri]
            page.title = title
            page.body = body
            page.uri = websafe_uri(title)
            PAGES[page.uri] = page
            url = request.route_url('page', title=page.uri)
            return HTTPFound(location=url)

    return {
        'title': title,
        'owner': page.owner,
        'body': body,
        'errors': errors,
    }

### CONFIGURE PYRAMID
def main(global_settings, **settings):
    config = Configurator(settings=settings)

    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        callback=groupfinder,
    )
    authz_policy = ACLAuthorizationPolicy()

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(Root)

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('users', '/users')
    config.add_route('user', '/user/{login}')

    config.add_route('pages', '/pages')
    config.add_route('create_page', '/create_page')
    config.add_route('page', '/page/{title}')
    config.add_route('edit_page', '/page/{title}/edit')

    config.include('pyramid_mako')
    config.scan(__name__)
    return config.make_wsgi_app()

### SIMPLE STARTUP
if __name__ == '__main__':
    settings = {
        'auth.secret': 'seekrit',
        'mako.directories': '%s:templates' % __name__,
    }
    app = main({}, **settings)

    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()

This is a demo intended to showcase Pyramid's authorization capabilities,
specifically for URL Dispatch.

Pyramid is abile to handle complex authorization using the
``ACLAuthorizationPolicy`` through the use of a ``resource tree``. By default,
Pyramid uses the resource tree for a lot of different tasks, but when looking at
URL Dispatch, the interesting aspect is the authorization. Thus, we treat the
resource tree as a hierarchy of permissions.

In this demo, your website will be split up into 2 different sections:

 * Managing/viewing the user accounts on the site.

 * Managing/viewing the pages of actual content.

So who has access to a given ``User``? We can add an ACL to the user defining
just that, and same with each ``Page`` in our site. The ACLs for these objects
can be found by traversing the resource tree using the urls::

    /users/{login}
    /pages/{page}

Your resource tree then becomes a hierarchy of permissions, where at any point
in the tree you can place an ``__acl__`` on a resource object::

    root (/)                   (Root)
    |- users                   (UserContainer)
    |  `- {login}              (User)
    `- pages                   (PageContainer)
       `- {page}               (Page)

You can represent this hierarchy in a resource tree::

    class Root(dict):
        # this is the root factory, you can set an __acl__ here for all resources
        __acl__ = [
            (Allow, 'admin', ALL_PERMISSIONS),
        ]
        def __init__(self, request):
            self.request = request
            self['users'] = UserContainer(self, 'users')
            self['pages'] = PageContainer(self, 'pages')

    class UserContainer(object):
        # set ACL here for *all* objects of type User,
        # in our example this also handles listing the users
        __acl__ = [
        ]

        def __init__(self, parent, name):
            self.__parent__ = parent
            self.__name__ = name

        def __getitem__(self, key):
            # get a database connection
            s = DBSession()
            obj = s.query(Foo).filter_by(id=key).scalar()
            if obj is None:
                raise KeyError
            obj.__parent__ = self
            obj.__name__ = key
            return obj

For the User we add in row-level permissions, allowing only the actual
user to view their data, any other user is disallowed.

::

    class User(object):
        # this __acl__ is computed dynamically based on the specific object
        @property
        def __acl__(self):
            return [
                (Allow, 'u:%s' % self.id, ('view', 'edit')),
            ]

    class PageContainer(object):
        # set ACL here for *all* objects of type Page,
        # in our example this also handles listing the users
        __acl__ = [
        ]

    class Page(object):
        # allow any authenticated user to view Page objects
        # but only allow the owner to edit the page
        __acl__ = [
            (Allow, Authenticated, 'view'),
            (Allow, 'u:%s' % self.owner_id, 'edit'),
        ]

With a setup like this, you can then map route patterns to your resource tree::

    config = Configurator()

    config.add_route('home', '/')

    config.add_route('users', '/users', traverse='/users')
    config.add_route('user', '/users/{login}', traverse='/users/{login}')

    config.add_route('pages', '/pages', traverse='/pages')
    config.add_route('page', '/pages/{page}', traverse='/pages/{page}')

Note we use the ``traverse=`` parameter to tell Pyramid where to find the
ACLs for the particular route. Without this, permissions would default to
the ACLs defined on the Root object.

You will also need to map your route to view handlers. This can be done two
different ways.

 * Using ``config.add_view`` explicitly::

    config.add_view(route_name='pages', view='.views.pages_view',
                    permission='view', renderer='pages.mako')

 * Using the ``@view_config`` decorator and invoking ``config.scan()``::

    # in your setup code:

    config.scan()

    # in your views package:

    @view_config(route_name='user', permission='view', renderer='user.mako')
    def user_view(request):
        #...

Great, now we can define our view and use the loaded context object, knowing
that if the view is executed, the user has the appropriate permissions!

::

    def user_view(request):
        user = request.context
        return {
            'user': user,
        }

Using this setup, you are using the default ``ACLAuthorizationPolicy``, and
you are providing row-level permissions for your objects with URL Dispatch.
Note also, that because the objects set the ``__parent__`` property on the
children, the policy will bubble up the lineage, inheriting the ACEs from the
parents. This can be avoided by simply putting a ``DENY_ALL`` ACE in your ACL,
or by writing a custom policy that does not use the context's lineage.

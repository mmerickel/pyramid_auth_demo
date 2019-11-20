.. _base_app:

================
Base Application
================

This is a basic wiki-style application. A visitor can view, add, and edit
pages. They can also login, logout and view information on users of the
system. The URL structure is as follows::

   /
   /login
   /logout

   /users
   /user/{login}

   /pages
   /create_page
   /page/{title}
   /page/{title}/edit

This demo isn't here to teach you how to use URL Dispatch or setup a
basic application. If you have any questions about how to setup this
simple application with no security, please go back to the Pyramid
documentation and tutorials to learn more.

Startup
=======

::

   python3 -m venv env
   env/bin/pip install pyramid pyramid-mako
   env/bin/python demo.py

Model
=====

The application is built around a model which persists ``User`` and
``Page`` objects.

Each ``User`` of the system has a `login`, `password`, and a list of
`groups` to which they belong.

.. literalinclude:: ../0.no_security/demo.py
   :pyobject: User

Each ``Page`` has a `title`, `body`, and `owner`, as well as a web-safe
`uri`.

.. literalinclude:: ../0.no_security/demo.py
   :pyobject: Page

Views
=====

Most of the views are cookie cutter, but views relating to authentication
have been singled out and explained in more detail.

Forbidden View
--------------

The `forbidden view` is an exception view registered for
``pyramid.httpexceptions.HTTPForbidden``. When a protected resource
is accessed with invalid permissions, Pyramid will raise an an
``HTTPForbidden`` exception. The base application provides two
possibilities, depending on whether the user is already logged in
when the permissions checks fail. If the user is not logged in they
are redirected to the `login` page. However, if they were already
logged in then we know they simply do not have access, and we return
the ``HTTPForbidden`` response (403 Forbidden).

.. literalinclude:: ../0.no_security/demo.py
    :pyobject: forbidden_view

Login View
----------

The `login view` will accept both `GET` and `POST` requests. On a `GET`
it will serve up the basic login page and on `POST` it will look in
the request's body for the ``login`` and ``password``, validate them
and if successful redirect to the previous page. A user is successfully
logged in by calling ``pyramid.security.remember`` which uses the
:term:`authentication policy` to generate a list of headers that should
be sent back as part of the `response`. These headers generally set a
cookie which will allow the application to track the user on subsequent
visits.

.. literalinclude:: ../0.no_security/demo.py
   :pyobject: login_view

Logout View
-----------

The `logout view` is very simple, but it showcases the use of
``pyramid.security.forget`` to generate a list of headers that should
be sent back as part of the `response`. These headers generally will
delete the cookies set by ``pyramid.security.remember``.

.. literalinclude:: ../0.no_security/demo.py
   :pyobject: logout_view

Create Page View
----------------

Unauthenticated users cannot create pages because a ``Page`` must
have an `owner`. This is protected by manually raising
``HTTPForbidden`` from *within* the ``create_page_view`` which will
invoke the `Forbidden View`_.

.. code-block:: python

   @view_config(route_name='create_page', renderer='edit_page.mako')
   def create_page_view(request):
       owner = request.authenticated_userid
       if owner is None:
           raise HTTPForbidden()

       # ...


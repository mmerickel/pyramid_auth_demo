Pyramid has the ability to handle complex authentication and authorization
patterns. How to do so is a constant source of frustration for new users. This
is a demo intended to showcase Pyramid's authorization capabilities. A lot of
the demo focuses on URL Dispatch. If you are interested in traversal, do not
despair as authorization via traversal is virtually indistinguishable from
the object-level security demo and all of the concepts learned transfer over
easily.

This demo is built around a wiki-style website to allows users to view and
create pages. The supported URL structure is as follows::

    /
    /login
    /logout

    /users
    /user/{login}

    /pages
    /create_page
    /page/{title}
    /page/{title}/edit

There are 3 different projects in this demo. Each project will add varying
levels of functionality to this application:

0. Base Application

   Allow anyone to do anything. This is the base website we'll be starting
   with to demonstrate different levels of security.

1. Group-Level Security

   Allow users different privileges based on their 'group'.

   For example, users 'michael' and 'chris' are in the 'admin' group, while
   'bob' is only in the 'user' group.

2. Object-Level Security

   Permit users access to all ``Page`` objects for which they are tagged
   as the owner, or permit a user to access only his or her ``User`` object.

   For example, 'michael' created the 'Demo' ``Page`` object, thus he can
   'edit' and 'delete' it. But he cannot 'edit' or 'delete' the 'Pyramid'
   ``Page`` because he is not the owner.

.. 3. Full Application
.. 
..    Look at how a real application can be configured around a ``User`` object
..    that is available on the current request. We will implement our own Pyramid
..    ``AuthenticationPolicy`` to have full control over its details. During
..    authentication, we will check the database to ensure that the ``User``
..    object still exists, disallowing deleted users from accessing the system.

Please reference the documentation in the `docs/` directory for explanations
of the different projects and levels of security. A rendered version of the
documentation can be found at
http://michael.merickel.org/projects/pyramid_auth_demo.

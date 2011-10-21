============
Introduction
============

Pyramid has the ability to handle complex authentication and authorization
patterns. How to do so is a constant source of frustration for new users.
This is a demo intended to showcase Pyramid's authorization capabilities.
A lot of the demo focuses on URL Dispatch. If you are interested in
traversal, do not despair as authorization via traversal is virtually
indistinguishable from the object-level security demo and all of the
concepts learned transfer over easily.

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

There are 4 different projects in this demo. Each project will add varying
levels of functionality to this application:

0. Base Application

   Allow anyone to do anything. This is the base website we'll be starting
   with to demonstrate different levels of security.

1. Group-Level Security

   Allow users different privileges based on their :term:`group` (aka
   their :term:`principal` identifiers).

   For example, users "michael" and "chris" are in the "admin" group, while
   "bob" is only in the "user" group.

2. Object-Level Security

   Permit users access to all ``Page`` objects for which they are tagged
   as the owner, or permit a user to access only his or her ``User`` object.

   For example, "michael" created the "Demo" ``Page`` object, thus he can
   "edit" and "delete" it. But he cannot "edit" or "delete" the "Pyramid"
   ``Page`` because he is not the owner.

3. Full Application

   Look at how a real application can be configured around a ``User`` object
   that is available on the current request. We will implement our own
   Pyramid :term:`authentication policy` to have full control over its
   details. During authentication, we will check the database to ensure
   that the ``User`` object still exists, disallowing deleted users from
   accessing the system.

Authentication vs Authorization
===============================

Pyramid's auth system is broken into 2 steps. First, an authenticated
user is identified and validated. Second, the system determines if the
user can access the requested resource. Below, we look at these 2 steps
separately.

Who are you?
------------

Identifying the current user when a :term:`request` enters the system is
the job of an :term:`authentication policy`. This is done in 3 steps:

1. Identify the user by inspecting tokens/headers/etc within the
   :term:`request`. (see ``unauthenticated_userid``)

   e.g. Parse the ``auth_token`` cookie of the request, check that it is
   properly signed, and return the detected user id ("bob").

2. Confirm and validate the status of the identified user.
   (see ``authenticated_userid``)

   e.g. Compare the unauthenticated user id against the database to ensure
   that the users credentials are still valid. Perhaps it had been deleted
   but an open browser still had a valid cookie. We'd want to prevent them
   from authenticating until they login again.

3. Map the user into a list of :term:`principal` identifiers. These
   commonly would include the user id, as well as a list of groups to
   which the user belongs. (see ``effective_principals``)

   e.g. Query the database for a list of groups to which the identified
   user belongs. Principals could be "bob", "user_admin", and "editor".

What can you do?
----------------

Each secure resource within Pyramid is protected by a :term:`permission`.
Determining which users have access to a resource is the job of an
:term:`authorization policy`.

From the previous section we have distilled the user down into a list of
:term:`principal` identifiers. The :term:`authorization policy` is then
passed the list of :term:`principal` identifiers and the :term:`permission`
and will either allow or deny access.

There is a third argument to the :term:`authorization policy` to assist
in resolving the required permission via the list of principals.
The :term:`context` is computed by traversing a :term:`resource tree`.
The :term:`context` can help to resolve the mapping between
:term:`principal` identifiers and a :term:`permission`. The use of a
:term:`resource tree` is described below.

The Resource Tree
=================

By default, Pyramid uses the :term:`resource tree` for a lot of different
tasks, but we're interested in how it can be used for security.

Thus, we treat the resource tree as a hierarchy of permissions.

Indices and tables
------------------

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. add a hidden toc to avoid warnings

.. toctree::
   :hidden:

   glossary


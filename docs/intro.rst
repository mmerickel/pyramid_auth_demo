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

Learn a little bit about how Pyramid's auth system works before diving
into the demo applications:

* :ref:`auth_vs_auth`
* :ref:`the_resource_tree`

This demo is built around a wiki-style website that allows users to view and
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

#. :ref:`base_app`

   Allow anyone to do anything. This is the base website we'll be starting
   with to demonstrate different levels of security.

#. :ref:`group_security`

   Allow users different privileges based on their :term:`group` (aka
   their :term:`principal` identifiers).

   For example, users "michael" and "chris" are in the "admin" group, while
   "bob" is only in the "user" group.

#. :ref:`object_security`

   Permit users access to all ``Page`` objects for which they are tagged
   as the owner, or permit a user to access only his or her ``User`` object.

   For example, "michael" created the "Demo" ``Page`` object, thus he can
   "edit" and "delete" it. But he cannot "edit" or "delete" the "Pyramid"
   ``Page`` because he is not the owner.

#. :ref:`full_app`

   Look at how a real application can be configured around a ``User`` object
   that is available on the current request. We will implement our own
   Pyramid :term:`authentication policy` to have full control over its
   details. During authentication, we will check the database to ensure
   that the ``User`` object still exists, disallowing deleted users from
   accessing the system.

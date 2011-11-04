.. _auth_vs_auth:

===============================
Authentication vs Authorization
===============================

Pyramid's auth system is broken into 2 steps. First, an authenticated
user is identified and validated. Second, the system determines if the
user can access the requested resource. Below, we look at these 2 steps
separately.

Who Are You?
============

Identifying the current user when a :term:`request` enters the system is
the job of an :term:`authentication policy`. This is done in 3 steps:

#. Identify the user by inspecting tokens/headers/etc within the
   :term:`request`. (see ``unauthenticated_userid``)

   e.g. Parse the ``auth_token`` cookie of the request, check that it is
   properly signed, and return the detected user id ("bob").

#. Confirm and validate the status of the identified user.
   (see ``authenticated_userid``)

   e.g. Compare the unauthenticated user id against the database to ensure
   that the users credentials are still valid. Perhaps it had been deleted
   but an open browser still had a valid cookie. We'd want to prevent them
   from authenticating until they login again.

#. Map the user into a list of :term:`principal` identifiers. These
   commonly would include the user id, as well as a list of groups to
   which the user belongs. (see ``effective_principals``)

   e.g. Query the database for a list of groups to which the identified
   user belongs. Principals could be "bob", "user_admin", and "editor".

What Can You Do?
================

Each secure resource within Pyramid is protected by a :term:`permission`.
Determining which users have access to a resource is the job of an
:term:`authorization policy`.

From the previous section we have distilled the user down into a list of
:term:`principal` identifiers. The :term:`authorization policy` will allow
or deny access based on those principals and the :term:`permission`.

Context-Level Security
----------------------

There is a third argument to the :term:`authorization policy` to assist
in resolving the required permission via the list of principals.
The :term:`context` is computed by traversing a :term:`resource tree`.
The :term:`context` can help to resolve the mapping between
:term:`principal` identifiers and a :term:`permission`. The use of a
:term:`resource tree` is described below.

What Can I Customize?
=====================

Almost everything. Both the authentication and authorization policies
are fully pluggable. The only thing in the system that is expected to
be pretty static are the permissions on the views, but how those are
mapped to access is completely configurable.

.. _object_security:

=====================
Object-Level Security
=====================

This demo builds on :ref:`group_security` by looking at how to implement
more fine-grained permissions. We'll be using Pyramid's default
:term:`authorization policy`, the ``ACLAuthorizationPolicy``.

Goals
=====

#. Maintain the previous group-level associations.
#. Allow editing of pages by the creator of the page.
#. Allow viewing of user-related pages by their respective users.

Why A Resource "Tree"?
======================

Trees provide a natural way to describe hierarchical data. This happens
to be, very often, how people think about permissions. If a user has
the "edit" permission on the node containing all ``Page`` objects in the
tree, then they usually also have the "edit" permission on the ``Page``
objects themselves, unless explicitly denied by a specific ``Page``
instance.

Our demo is focused on a resource tree similar to the following::

   root (/)                   (Root)
   |- users                   (UserFactory)
   |  `- {login}              (User)
   `- pages                   (PageFactory)
      `- {page}               (Page)

Except that in order to illustrate the usage of the multiple factories,
the individual branches are broken into their own individual trees.
The downside to breaking up the tree is that there is no longer a
common location to provide a default ACL, for example to simply give
full access to "admin" users. On the flip side, the trees become
much simpler to understand as they are more focused.

Location-Aware Resources and Hierarchical Permissions
-----------------------------------------------------

The ``ACLAuthorizationPolicy`` works on this idea by supporting
cascading ACLs. Remember that the ``ACLAuthorizationPolicy`` operates
on 3 parameters, the principals, the permission and the :term:`context`.
The context is the last node traversed in the resource tree and it is
the first place the policy checks for an ACL. If no matching entry is
found, the policy will then recursively check the parent of the context
for an ACL and matching entry, bubbling up the tree until it hits the
root. In this way, hierarchical permissions are automatically handled
when organizing resources and ACLs into a :term:`resource tree`.

The ``ACLAuthorizationPolicy`` can recursively travel through the
lineage from the context to the root due to what Pyramid calls
`location-aware` resources, meaning they implement the ``__parent__``
and ``__name__`` attributes.

Disabling Hierarchical Permissions
----------------------------------

The cascading nature of the tree can be prevented in 2 simple ways
without replacing the ``ACLAuthorizationPolicy`` with a different
implementation.

#. Add an entry at the end of each ACL for ``pyramid.security.DENY_ALL``
   which is effectively an alias for the entry
   ``(Deny, Everyone, ALL_PERMISSIONS)``. If no matching entry is found
   in the ACL prior to this entry, then this one will match effectively
   preventing the policy from going any further.
#. Do not create `location-aware` resources. i.e. Do not add
   ``__parent__`` properties to your resources.

Resource Factories
==================

From the :ref:`group_security` demo we saw how to create a single-node
:term:`resource tree` that could map a user's list of :term:`principal`
identifiers to the ``__acl__`` property of the ``Root``, resulting in
either being allowed or denied access to a :term:`resource` based on
the required :term:`permission`.

It's actually possible to have many resource trees in a single Pyramid
application. The :term:`root factory`, supplied with the request object,
can return the root of any tree it wishes. Each route, when using URL
Dispatch, can also define its own factory. It's this last point that
we'll explore further.

As Pyramid processes an incoming request, the :term:`router` first
finds a matching route for the requested URL, then performs
:term:`traversal` on the resource tree returned from the root factory.
If the route itself does not define a factory, the default root factory
will be used to compute the resource tree. There are actually 4
possibilities for the path used in traversal.

#. If no route is matched, traversal occurs on the URL path.
#. If a route is matched and the route defines a ``*traverse`` pattern,
   the matching part of the URL will be used.
#. If a route is matched and the route defines a ``traverse`` argument
   then the supplied path will be traversed.
#. If a route is matched and no traversal path has been defined then
   traversal occurs effectively on the ``/`` path, returning the root
   of the tree as the context. Note that this is how the
   :ref:`group_security` demo is configured.

Why Is This Interesting?
------------------------

An URL in a "REST"-y world (to beat a dead term) is intended to focus
on a single resource. This maps very well to Pyramid's concept of
traversing a tree of resources. Object-level security can be thought
of in this way, where the resource in question is modifiable by
specific users (actually principals). We can define a
:term:`root factory` that knows how to load a specific type of resource
and attach it to only relevant URLs. Examples of this idea are shown
below.

Securing the Views
==================

The only change between the object-level demo and the group-level demo
from the previous section are how the ACLs are computed. The permission
on each view remains unchanged.

.. note::

   Because traversal is loading the actual objects from the model to
   determine the ACL, the views no longer need to explicitly load those
   objects. Instead they can just use the ``context`` which will be
   a ``User`` or ``Page`` object. This of course only works for loading
   of simple objects, more complex queries would still need to be done
   within the views themselves.

User Pages
----------

For user-related pages in our application, our goal was to secure
them based on the relationship between the currently logged in user
and the requested user's page. We'll use a simple resource tree with
only one branch, traversed via the path ``'/{login}'``.

User Factory
~~~~~~~~~~~~

For these pages we can use the ``UserFactory`` to provide default ACL
for any user page.

.. literalinclude:: ../2.object_security/demo.py
   :pyobject: UserFactory

User Resources
~~~~~~~~~~~~~~

A ``User`` object is created and returned by the ``UserFactory`` based
on the ``login`` property. A ``User`` resource should only be
accessible by the user itself, or an "admin" (which we've covered
already in the ``UserFactory``). To enable this object-level access to
the specific resource, the ``User`` implements a dynamic ``__acl__``
by turning the class variable into a property which can be computed
per-instance of the object. The new ACL contains an entry for a
principal matching the ``login`` property of the object.

.. literalinclude:: ../2.object_security/demo.py
   :lines: 19-24

Defining the Routes
~~~~~~~~~~~~~~~~~~~

Traversal of the new tree is done by configuring the user-related
routes to use the new ``UserFactory`` instead of the default ``Root``
factory.

.. literalinclude:: ../2.object_security/demo.py
   :lines: 324-326

The ``'user'`` route also overrides the ``traverse`` parameter to
load the ``User`` object for that URL. The matched ``login`` in the
route will be substituted into the traversal path. For example, a
request for the ``'/user/michael'`` URL, will cause the traversal
path to be ``'/michael'``.

Wiki Pages
----------

The biggest change to the wiki pages is giving the creator of the page
the ability to edit it, even if they aren't in the "editor" group. The
resource tree is a single branch traversed via the path ``'/{title}'``.

Page Factory
~~~~~~~~~~~~

For these pages we can use the ``PageFactory`` to provide default ACL
for any wiki page.

.. literalinclude:: ../2.object_security/demo.py
   :pyobject: PageFactory

Page Resources
~~~~~~~~~~~~~~

A ``Page`` object is created and returned by the ``PageFactory`` based
on the ``uri`` property. A ``Page`` resource should only be
editable by the creator, an "editor" or an "admin" (which we've covered
already in the ``PageFactory``). To enable this object-level access to
the specific resource, the ``Page`` implements a dynamic ``__acl__``
by turning the class variable into a property which can be computed
per-instance of the object. The new ACL contains an entry for a
principal matching the ``owner`` property of the object.

.. literalinclude:: ../2.object_security/demo.py
   :lines: 34-40

Defining the Routes
~~~~~~~~~~~~~~~~~~~

Traversal of the new tree is done by configuring the wiki-related
routes to use the new ``PageFactory`` instead of the default ``Root``
factory.

.. literalinclude:: ../2.object_security/demo.py
   :lines: 328-333

The ``'page'`` and ``'edit_page'`` routes also override the
``traverse`` parameter to load the ``Page`` object for that URL. The
matched ``title`` in the route will be substituted into the traversal
path. For example, a request for the ``'/page/hello'`` URL, will cause
the traversal path to be ``'/hello'``.

Summary
=======

We've seen how to build different resource trees into different parts
of our site, as well as how to configure hierarchical permissions via
the structure of the tree and `location-aware` resources.

Object or row-level security on ``User`` and ``Page`` objects was
achieved via dynamic ACLs on the respective objects.

Isn't This Just Traversal? Why Even Bother With URL Dispatch?
-------------------------------------------------------------

It's very close to traversal. The traversal machinery is executed
whether using URL Dispatch or Traversal. The difference is simply how
`view lookup` occurs. When using Traversal, the computed context and
view name are the key factors in determining which view is executed. In
URL Dispatch it is dependent on which route matched and the context is
used in the background almost purely for security purposes.

A lot of times we may not have full control over our URLs due to legacy
code, or just disagreements on design. In those cases it's still
important to provide a way to map those routes to resources in our
system and the custom ``factory`` and ``traverse`` arguments allow for
that level of customization.

Where To Go From Here?
----------------------

Pyramid's entire auth system is pluggable. Almost all of the examples
of authorization depend on the ``ACLAuthorizationPolicy`` because it is
so flexible. However, it could be replaced with something that did
group or object lookup independent of the actual traversal context, or
it could give an entirely new meaning to the context in terms of
security.

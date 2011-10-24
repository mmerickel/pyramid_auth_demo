.. _the_resource_tree:

=================
The Resource Tree
=================

Pyramid has excellent documentation on using the :term:`resource tree`,
especially for traversing a URL and mapping it to a view. This will not
attempt to duplicate that, but rather provide a simplified explanation
specifically for security.

Root Factory
============

Resources are organized into a tree of objects that are traversed using a
path (``'/foo/bar/baz'``). Each :term:`resource` is expected to implement
the ``__getitem__`` method and return the next resource in the tree. Pyramid
uses a factory which, given the current request object, returns the root of
the tree. Returning a different tree per request is completely valid.
Below are two examples of factories that return a ``Resource`` instance as
the root of the tree.

.. code-block:: python

    class Resource(object):
        def __getitem__(self, key):
            raise KeyError

    class RootFactory(Resource):
        def __init__(self, request):
            self.request = request

    def root_factory(request):
        return Resource()

Traversal
=========

A path is broken into its segments and used to traverse the
:term:`resource tree`. For example the path ``'/foo/bar/baz'`` is split
into a 3-tuple ``('foo', 'bar', 'baz')``. The segments are then used
to traverse the tree via the ``__getitem__`` methods of the successive
resources. Below is an example of a simple tree that drills down into
a corporation's hierarchy.

.. code-block:: python

    class Employee(object):
        pass

    class Department(object):
        def __getitem__(self, key):
            emp = Employee()
            emp.id = key
            return emp

    class Corporation(object):
        def __getitem__(self, key):
            dept = Department()
            dept.id = key
            return dept

    class Root(object):
        def __getitem__(self, key):
            corp = Corporation()
            corp.id = key
            return corp

    def root_factory(request):
        return Root()

Using this setup, Pyramid will use the ``root_factory`` to create the
``root`` which will then be used to traverse the tree. The resulting
``context`` will be an instance of the ``Employee``.

.. code-block:: python

    >>> root = root_factory(None)
    >>> context = root['acme']['weapons']['coyote']
    >>> context
    <Employee object at ...>

If at any point an invalid ``key`` is supplied, a ``KeyError`` exception can
be raised which will end the traversal. The last valid resource in the
tree will then be used as the ``context``. However, in our simple example
any (corporation, department, employee) combination will be accepted.

Security
========

Traversal allows for a completely natural way to organize a hierarchy
of objects. It also happens to be the way a lot of applications think
about security and permissions. For example, if we use the
:term:`resource tree` from the previous section, it looks remarkably like
a security hierarchy we might use within our site. If a user is part of a
corporation they can ``view`` the departments, but unless they are in
management they cannot ``create``, ``update`` or ``destroy`` them. Going
further, an employee can ``update`` its own records but no one elses.

The implementations of :ref:`group-level <group_security>` and
:ref:`object-level <object_security>` security are covered in their own
sections.

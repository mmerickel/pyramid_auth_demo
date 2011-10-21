.. _glossary:

Glossary
========

.. glossary::
   :sorted:

   Pyramid
     A `web framework <http://www.pylonsproject.org>`_.

   request
     An object that represents an HTTP request.

   group
     An alias for :term:`principal` which is more commonly used in the
     context of group-level security.

   principal
     A *principal* is a string or unicode object representing a userid
     or a group id.  It is provided by an authentication policy.
     For example, if a user had the user id "bob", and Bob
     was part of two groups named "group foo" and "group bar", the
     request might have information attached to it that would
     indicate that Bob was represented by three principals: "bob",
     "group foo" and "group bar".

   permission
     A string or unicode object that represents an action being taken
     against a :term:`context` resource.  A permission is associated with
     a view by the developer. Example permissions might be "read", "edit",
     or "view_blog_entries".

   authorization policy
     The API which determines whether or not the principals associated
     with the request can perform an action associated with a permission.

   authentication policy
     The API which determines the current :term:`principal`
     (or principals) associated with a request.

   resource
     An object representing a node in the :term:`resource tree` of an
     application.

   resource tree
     A nested set of dictionary-like objects, each of which is a
     :term:`resource`. The act of :term:`traversal` uses the resource tree
     to find a :term:`context` resource.

   context
     A resource in the :term:`resource tree` that is found during
     :term:`traversal`. A context resource often has security information
     attached to it.

   traversal
     The act of descending "up" a tree of resource objects from a root
     resource in order to find a :term:`context` resource.



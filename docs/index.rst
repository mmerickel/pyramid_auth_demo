.. _index:

Pyramid Auth Demo
=================

Pyramid has the ability to handle complex authentication and authorization
patterns. How to do so is a constant source of frustration for new users.
This is a demo intended to showcase Pyramid's authorization capabilities.
A lot of the demo focuses on URL Dispatch. If you are interested in
traversal, do not despair as authorization via traversal is virtually
indistinguishable from the object-level security demo and all of the
concepts learned transfer over easily.

This demo is built around a wiki-style website that allows users to view
and create pages. All of the code for each demo is available on GitHub
at `<https://github.com/mmerickel/pyramid_auth_demo>`__ and should be used
to follow along as only certain parts of each demo are shown in the
narrative.

.. toctree::
   :maxdepth: 2

   intro
   auth_vs_auth
   resource_trees
   base_app
   group_security
   object_security
   full_app

Indices and tables
==================

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. add a hidden toc to avoid warnings

.. toctree::
   :hidden:

   glossary


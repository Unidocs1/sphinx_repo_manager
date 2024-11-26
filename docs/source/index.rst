Sphinx Repo Manager
===================

Hello World
-----------

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   content/-/index
   content/demo_doc/index
   content/demo_doc/RELEASE_NOTES

Included Content Demo
~~~~~~~~~~~~~~~~~~~~~

* When you have repos symlinked to ``content/{repo_name}``, use the ``include`` directive for this initial entry point
  to separate all context from logic. 

* If you use the ``:start-after:`` include option, you can skip content you may not want (like a duplicate header)
  that may appear when testing the standalone repo *without* ``sphinx_repo_manager``:

.. code-block::

   .. include:: content/demo_doc/index.rst
      :start-after: start-marker

As long as you declare a ``.. start-marker`` directive right above where your content starts.

.. include:: content/demo_doc/index.rst
   :start-after: start-marker

Resources
---------

* `Source code <https://gitlab.acceleratxr.com/Core/xbe_docs>`_
* Production-grade `implementation demo <https://source.goxbe.io/Core/docs/xbe_static_docs>`_
* Questions? Ask us in `Discord <https://discord.gg/xsollabackend>`_

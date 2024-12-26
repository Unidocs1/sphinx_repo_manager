Sphinx Repo Manager
===================

Hello World
-----------

Table of Contents: 

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   content/-/index
   content/sphinx_demo_doc/index
   content/sphinx_demo_doc/RELEASE_NOTES

Included Content Demo
~~~~~~~~~~~~~~~~~~~~~

* When you have repos symlinked to ``content/{repo_name}``, use the ``include`` directive for this initial entry point
  to separate all context from logic. 

* If you use the ``:start-after:`` include option, you can skip content you may not want (like a duplicate header)
  that may appear when testing the standalone repo *without* ``sphinx_repo_manager``:

.. code-block::

   .. include:: content/sphinx_demo_doc/index.rst
      :start-after: start-marker

As long as you declare a ``.. start-marker`` directive right above where your content starts.

.. include:: content/sphinx_demo_doc/index.rst
   :start-after: start-marker

Resources
---------

* sphinx_repo_manager `source code <https://source.goxbe.io/Core/docs/sphinx_repo_manager>`__

   * Note ``/docs`` if inspecting this build demo

* (This) sphinx_demo_doc `source code <https://source.goxbe.io/Core/docs/sphinx_demo_doc>`__
* Production-grade `implementation demo <https://source.goxbe.io/Core/docs/xbe_static_docs>`__

   * Note ``docs/repo_manifest.yml`` for an *advanced* manifest demo

* Questions? Ask us in `Discord <https://discord.gg/xsollabackend>`__

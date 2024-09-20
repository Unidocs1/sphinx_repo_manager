:og:title: Welcome to Xsolla Backend
:og:description: Xsolla Backend is a powerful backend engine for building highly-scalable online games and entertainment products - pay only 5% for unlimited support and enterprise features.
:og:image: /_static/images/_local/xbe-banner-og-1200x630.min.png

.. meta::
   :description: Xsolla Backend [XBE] is a powerful backend engine for building highly-scalable online games and entertainment products covering a robust set of features - pay only 5% for unlimited support and enterprise features
   :keywords: xbe, xsolla backend, axr, acceleratxr, backend, backend as a service, gbaas, doc, docs, api docs, api, openapi, xbe docs, xsolla docs, xsolla backend docs

=========================
Welcome to Xsolla Backend
=========================

.. image:: /_static/images/_local/xbe-banner-og-1200x478.min-smLogoNoTxt.png
   :alt: XBE Docs
   :width: 720px

.. TIPS:
.. xbe_static_docs content can be found symlinked to <content/-/> for shorter url slugs. Eg: <content/-/welcome/index>
.. This is possible due to repo_manifest.yml `init_clone_path_root_symlink_src_override: 'docs/source/content'`

.. feature-flag:: production-stage
   :fallback:

   .. toctree:: 
      :caption: (!) Dev
      :hidden:
   
      (!) All Repo Docs <content/-/_dev/all_repo_docs>
      (!) All Architecture Docs <content/-/_dev/all_architecture_docs>
      (!) All Performance Docs <content/-/_dev/all_performance_docs>
      (!) All Tutorial Docs <content/-/_dev/all_tutorial_docs>
      (!) All Static Docs <content/-/index>

.. feature-flag:: use-new-price-page-url

   .. toctree:: 
      :caption: Welcome
      :hidden:
      
      About XBE <content/-/welcome/what_is_xbe>
      Features <content/-/welcome/features>
      Quickstart <content/-/welcome/quickstart>
      Demo <content/-/welcome/demo_env>
      Release Notes <content/-/welcome/release_notes/current/index>
      Create Your Account <https://xsolla.cloud>

.. feature-flag:: use-new-price-page-url
   :fallback:

   .. toctree:: 
      :caption: Welcome
      :hidden:
      
      About XBE <content/-/welcome/what_is_xbe>
      Features <content/-/welcome/features>
      Quickstart <content/-/welcome/quickstart>
      Demo <content/-/welcome/demo_env>
      Release Notes <content/-/welcome/release_notes/current/index>
      Create Your Account <https://www.acceleratxr.com/pricing>

.. toctree::
   :caption: Components
   :hidden:

   Components Overview <content/-/components/index>
   Accounts <content/-/components/accounts/index>
   Content <content/-/components/content/index>
   Economy <content/-/components/economy/index>
   Gameplay <content/-/components/gameplay/index>
   Multiplayer <content/-/components/multiplayer/index>
   Storefront <content/-/components/storefront/index>
   System <content/-/components/system/index>
   Monitoring <content/-/components/monitoring/index>

.. toctree::
   :caption: Learning Essentials
   :hidden:

   Framework Concepts <content/-/how_to/framework_concepts/index>
   Install <content/-/how_to/install/index>
   Administration <content/-/how_to/admin/index>
   Tutorials <content/-/how_to/tutorials/index>
   Full Game Samples <content/-/how_to/full_game_samples/index>
   API Docs <content/-/api/index>

.. toctree::
   :caption: SDK
   :hidden:

   SDK Overview <content/-/sdk/index>
   Unreal SDK <content/-/sdk/sdk_unreal_ref>
   Unity SDK <content/-/sdk/sdk_unity_ref>

.. toctree::
   :caption: Legal / Contact
   :hidden:
   
   EULA <content/-/legal/eula/index>
   Chat With Us! <https://discord.gg/XsollaBackend>

.. include:: component_cards-partial.rst
   :start-after: start-marker

Xsolla Backend [XBE] is a powerful backend engine for building highly-scalable online games and entertainment
products. XBE's robust set of :doc:`features <content/-/welcome/features>` cover everything you need - from
matchmaking and identity to quest systems - enabling you to craft modern online experiences quickly and affordably:

* **Pay only 5%** of gross sales paid
* **Free** Hosting
* **Source** Available
* **Unlimited** Support
* **Enterprise** Features

.. raw:: html

   <a class="xsui-button xsui-button--appearance-secondary xsui-button--size-sm" href="content/-/welcome/what_is_xbe.html">
      <div class="xsui-button__wrapper">
         <div class="xsui-button__content">Learn More</div>
      </div>
   </a>

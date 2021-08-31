============================
How to Create a Level System
============================

This guide will show you how to create a linear skill tree whereby a set of skills directly follow from one to the next in a set. To illustrate this we will create a simple leveling system with ten levels. The levels are defined as skill definitions and then a single archetype serves as a single classification for the entire level system.

Pre-requisites
--------------

This guide assumes you have read and understand the following documents:


* `Concepts <concepts>`_
* `EventProcessor <processor>`_
* `REST API: SkillDefinition <restapi/routes/SkillDefinitionRoute>`_
* `REST API: ArchetypeDefinition <restapi/routes/ArchetypeDefinitionRoute>`_

Events
------

In order to make a proper leveling system we will need to track two types of telemetry events: ``GainXP`` and ``SkillUnlocked``. The ``GainXP`` is a custom event type we will use to track the amount of experience a given persona has earned over time. The ``SkillUnlocked`` event type is used to chain a set of levels together so that level 10 follows 9 which follows level 8 and so on.

Whenever a persona has earned experience an event will be sent to the ``telemetry_services`` system with the type ``GainXP`` and the ``value`` property set to the amount of experience actually earned.

This can be implemented as a server side feature (recommended) or by the client directly.

Sending events from a service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: typescript

   const data: any = {
       type: "GainXP",
       userId: user.uid,
       personaUid: user.personas[0].uid,
       value: 100,
   };
   EventUtils.record(new Event(config, user.uid, data));

Sending events from the SDK
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: csharp

   Event eventObj = new Event
   {
       Type = "GainXP",
       UserId = ClientSDK.LoggedInUser.uid,
       PersonaUid = ClientSDK.LoggedInUser.personas[0].uid,
       Value = 100
   };
   EventService eventService = ServiceFactory.GetService<EventService>();
   await eventService.Create(eventObj);

.. code-block:: cpp

   std::shared_ptr<models::Event> eventObj(new models::Event);
   eventObj->SetType("GainXP");
   eventObj->SetUserUid(ClientSDK.LoggedInUser.uid);
   eventObj->SetPersonaUid(ClientSDK.LoggedInUser.personas[0].uid);
   eventObj->Set("value", 100);
   auto eventService = ServiceFactory::GetInstance()->GetService<services::EventService>();
   eventService->Create(eventObj).Wait();

Defining Levels as Skills
-------------------------

Now that we have a mechanism to track experience we can define our levels. Each level has have an associated skill definition where the requirements include the amount of relative experience that must be reached (from the prior level) as well as the previous level that must be required.

The first level in our system is very simple as it has no requirements. All players must start at level 1. Thus the skill definition looks as follows.

.. code-block:: typescript

   {
       uid: "e744aba4-e07e-43aa-bfb2-5ffe8cf064eb",
       name: "level_1",
       title: "Level 1",
       description: "You are level 1.",
       icon: "level1.png",
       requirements: [],
   }

In order to create this definition with the service we send a ``POST`` request to the ``/skills`` endpoint containing the above as the payload.

.. code-block::

   POST /skills HTTP/1.1
   Authorization: jwt <admin_token>
   Content-Type: application/json

   {
       name: "level_1",
       title: "Level 1",
       description: "You are level 1.",
       icon: "level1.png",
       requirements: [],
   }

For level two we will add some experience as the sole requirement. We will choose a value of ``1000`` which means that at ten of the aforementioned events would need to be created in order to unlock the level.

.. code-block:: typescript

   {
       uid: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
       name: "level_2",
       title: "Level 2",
       description: "You are level 2.",
       icon: "level2.png",
       requirements: [
           {
               type: "GainXP",
               title: "Earn experience",
               description: "Requires 1000 experience.",
               icon: "xp.png",
               value: 1000,
           },
       ],
   }

Just like the level 1 we create this definition by ``POST``\ ing to the ``/skills`` endpoint.

.. code-block::

   POST /skills HTTP/1.1
   Authorization: jwt <admin_token>
   Content-Type: application/json

   {
       uid: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
       name: "level_2",
       title: "Level 2",
       description: "You are level 2.",
       icon: "level2.png",
       requirements: [
           {
               type: "GainXP",
               title: "Earn experience",
               description: "Requires 1000 experience.",
               icon: "xp.png",
               value: 1000,
           },
       ],
   }

For level 3 we will set an experience requirement as well as a ``SkillUnlocked`` requirement chaining it to level 2. Note that the ``value`` of the requiremnt will be the ``uid`` of the level two skill definition which in the above example is ``1ea968f3-ca97-4d8c-8c9d-63d183942be0``. This level will require ``5000`` experience points to achieve.

.. code-block:: typescript

   {
       uid: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
       name: "level_3",
       title: "Level 3",
       description: "You are level 3.",
       icon: "level3.png",
       requirements: [
           {
               type: "GainXP",
               title: "Earn experience",
               description: "Requires 1000 experience.",
               icon: "xp.png",
               value: 5000,
           },
           {
               type: "SkillUnlocked",
               title: "Level 2",
               description: "Requires level 2.",
               icon: "level2.png",
               value: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
           },
       ],
   }

We can now create the remaining levels the same way as level 3, where the ``SkillUnlocked`` requirement references the level before it. Our final level, level 10 will thus look like the following.

.. code-block:: typescript

   {
       uid: "d0e030c7-c6c1-489f-9096-2c17285b4961",
       name: "level_10",
       title: "Level 10",
       description: "You are level 10.",
       icon: "level10.png",
       requirements: [
           {
               type: "GainXP",
               title: "Earn experience",
               description: "Requires 1000 experience.",
               icon: "xp.png",
               value: 100000,
           },
           {
               type: "SkillUnlocked",
               title: "Level 9",
               description: "Requires level 9.",
               icon: "level9.png",
               value: "351b9c8d-1773-464e-9d46-e5eb777ed6ed",
           },
       ],
   }

Creating the Archetype Definition
---------------------------------

It is necessary to create an archetype for our set of levels. The archetype contains descriptive information about it as well as a list of the root skills in the tree. In this case, our root skills are level 1 and level 2. The system automatically traverses these root skills for children referenced as requirements to build the large tree(s).

.. code-block:: typescript

   {
       name: "levels",
       title: "Levels",
       description: "All levels that persona can achieve.",
       icon: "levels.png",
       skills: [
           "e744aba4-e07e-43aa-bfb2-5ffe8cf064eb",
           "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
       ],
   }

Note that if level 2 is modified to incldue level 1 as a requirement then list of skills for the archetype can be reduced to only level 1.

The archetype is then created by sending a ``POST`` request to the ``/archetypes`` endpoint.

.. code-block::

   POST /archetypes HTTP/1.1
   Authorization: jwt <admin_token>
   Content-Type: application/json

   {
       uid: "a3708071-cd11-498c-a886-29e089d859c0",
       name: "levels",
       title: "Levels",
       description: "All levels that persona can achieve.",
       icon: "levels.png",
       skills: [
           "e744aba4-e07e-43aa-bfb2-5ffe8cf064eb",
           "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
       ],
   }

Enabling an archetype for a given persona
-----------------------------------------

Now that our levels system has been created we can now enable it for personas so that they start tracking progress.

To enable an archetype for a given persona a ``PUT`` request is sent to the ``PUT /personas/{personaUid}/archetypes/{archetypeUid}`` endpoint. The request requires a payload containin the ``enabled`` state to set.

As an example imagine we have a persona with uid ``4d1710e8-912e-4671-94d2-eaf51c301dcf``. The request to enable the levels archetype would thus be.

.. code-block::

   POST /personas/4d1710e8-912e-4671-94d2-eaf51c301dcf/archetypes/a3708071-cd11-498c-a886-29e089d859c0 HTTP/1.1
   Authorization: jwt <user_token>
   Content-Type: application/json

   {
       enabled: true
   }

Retrieving Enabled Archetypes
-----------------------------

Once an archetype has been enabled for a given persona it is possible to retrieve the complete definition of the archetype including the entire tree of skills associated with it by performing a ``GET`` request to the ``GET /personas/{personaUid}/archetypes/{archetypeUid}`` endpoint.

For our above example this request would look like.

.. code-block::

   GET /personas/4d1710e8-912e-4671-94d2-eaf51c301dcf/archetypes/a3708071-cd11-498c-a886-29e089d859c0 HTTP/1.1
   Authorization: jwt <user_token>

The response of the above request will look like the following.

.. code-block:: typescript

   {
       uid: "a3708071-cd11-498c-a886-29e089d859c0",
       name: "levels",
       title: "Levels",
       description: "All levels that persona can achieve.",
       icon: "levels.png",
       skills: [
           {
               name: "level_1",
               title: "Level 1",
               description: "You are level 1.",
               icon: "level1.png",
               requirements: [],
           },
           {
               uid: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
               name: "level_2",
               title: "Level 2",
               description: "You are level 2.",
               icon: "level2.png",
               requirements: [
                   {
                       type: "GainXP",
                       title: "Earn experience",
                       description: "Requires 1000 experience.",
                       icon: "xp.png",
                       value: 1000,
                   },
               ],
           },
           {
               uid: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
               name: "level_3",
               title: "Level 3",
               description: "You are level 3.",
               icon: "level3.png",
               requirements: [
                   {
                       type: "GainXP",
                       title: "Earn experience",
                       description: "Requires 1000 experience.",
                       icon: "xp.png",
                       value: 5000,
                   },
                   {
                       type: "SkillUnlocked",
                       title: "Level 2",
                       description: "Requires level 2.",
                       icon: "level2.png",
                       value: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
                   },
               ],
           },
           ...
           {
               uid: "d0e030c7-c6c1-489f-9096-2c17285b4961",
               name: "level_10",
               title: "Level 10",
               description: "You are level 10.",
               icon: "level10.png",
               requirements: [
                   {
                       type: "GainXP",
                       title: "Earn experience",
                       description: "Requires 1000 experience.",
                       icon: "xp.png",
                       value: 100000,
                   },
                   {
                       type: "SkillUnlocked",
                       title: "Level 9",
                       description: "Requires level 9.",
                       icon: "level9.png",
                       value: "351b9c8d-1773-464e-9d46-e5eb777ed6ed",
                   },
               ],
           }
       ],
   }

Retrieving Skill Progress
-------------------------

The current progress of a persona for a given archetype can be retrieved using the ``/personas/{personaUid}/archetypes/{archetypeUid}/skills`` endpoint.

.. code-block::

   GET /personas/4d1710e8-912e-4671-94d2-eaf51c301dcf/archetypes/a3708071-cd11-498c-a886-29e089d859c0/skills HTTP/1.1
   Authorization: jwt <user_token>

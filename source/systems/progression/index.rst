==================
Progression System
==================

.. toctree::
  :hidden:

  processor

Overview
========

This progression system provides a RESTful service for the management of developer designed skills and archetypes. A skill is any level, talent, or other construct that gives the persona an ability to perform some action within the product. In a typical MMORPG this may be a damage spell, a weapon attack or a healing potion. An archetype is a grouping of skills that can be enabled for a given persona. This makes it possible to create classifications of skills such as levels or classes (e.g. Mage, Warrior, etc) in a typical RPG title. When a given persona enables an specific archetype, all of the skills associated with that archetype are enabled for the persona. However, an enabled skill does not necessarily mean that the persona can use the skill. Skills must be unlocked by meeting their requirements. Only enabled skills are eligible to track progress and be unlocked. The system also allows switching of enabled status on archetypes, thus allowing scenarios such as class re-assignment. There are no limits to the number of archetypes that can be active at any given time for a single persona.

Skill requirements and their progress are tracked using the ``telemetry_services`` system. When defining a given skill requirement you must specify a ``type``. This ``type`` property must match a telemetry event thats has both a ``type`` and ``value`` field. The service will also generate events of it's own such as ``SkillActivated``\ , ``SkillDeactivated``\ , and ``SkillUnlocked``. This allows other skills to be used as requirements thereby making it possible to create rich, tree-like skill structures with multiple branching paths. Despite a slight delay in the processing time of events, by leveraging the telemetry system for the tracking of this progress it reduces the chance for cheating. It is also possible to post progress updates directly for a given skill if a real-time system is desired.

The service composes three primary parts; the REST API that manages skill definitions, archetypes and a persona's set of skills, an event scraper and an event processor.

The REST API is used to define the definition of a given set of available skills, archetypes as well as the skills associated with a particular persona.

The `\ ``EventScraper`` <scraper>`_ is a background service used to retrieve telemetry events from the `\ ``telemetry_services`` </docs/telemetry_services>`_ system that is used by the `\ ``EventProcessor`` <processor>`_. Events retrieved that are scraped are placed into a global redis queue which any instance of the service can process.

Once an event is placed in the global queue, the `\ ``EventProcessor`` <processor>`_ pops it and begins processing the event. The processor first identifies all quests that reference the event type as a requirement and then uses it to update either the unlock progress or the primary progress of the quest for the given player.

Data Structures
---------------

SkillDefinition
^^^^^^^^^^^^^^^

The skill definition is the developer created concept of an individual skill within the system. The definition includes descriptive information about a given skill such as the ``title``\ , ``description`` and ``icon`` as well as the list of ``requirements`` that are needed for a persona to unlock access to the skill. A special ``data`` field is also provided allowing products to add customizeable information to each skill definition. This is useful when it is desired to encode information such as damage, cooldowns, and other game specific attributes.

.. list-table::
   :header-rows: 1

   * - Member
     - Description
     - Type
     - Format / Schema
     - Default Value
     - Identifier
     - Unique
     - Required
   * - `uid <#uid>`_
     - The universally unique identifier of the object.
     - ``string``
     - uuid
     - ``uuid.v4()``
     - true
     - true
     - true
   * - `dateCreated <#dateCreated>`_
     - The date and time that the object was created.
     - ``string``
     - date-time
     - ``now()``
     - false
     - false
     - true
   * - `dateModified <#dateModified>`_
     - The date and time that the object was last modified.
     - ``string``
     - date-time
     - ``now()``
     - false
     - false
     - true
   * - `version <#version>`_
     - The optimistic locking version of the object.
     - ``integer``
     - 
     - ``0``
     - false
     - false
     - true
   * - `name <#name>`_
     - The unique name of the skill.
     - ``string``
     - 
     - ``""``
     - true
     - true
     - true
   * - `title <#title>`_
     - A textual title or name of the skill.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `description <#description>`_
     - A textual description of the skill.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `icon <#icon>`_
     - The icon to display when representing the skill.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `requirements <#requirements>`_
     - The list of requirements that the persona must fulfill to unlock the skill.
     - ``array``
     - 
     - ``
     - false
     - false
     - true
   * - `data <#data>`_
     - Stores any custom data to be used by the product.
     - ``object``
     - 
     - ``undefined``
     - false
     - false
     - true


SkillRequirement
^^^^^^^^^^^^^^^^

Each skill definition contains a list of requirements. These requirements must be met in order for a persona to unlock the skill to be used. The requirement has similar descriptive information allowing products to provide rich text about each requirement. The ``type`` property is used to identify a particular telemetry event that will trigger completion of the requirement with the ``value`` being the desired value to meet.

Skill requirements and their progress are tracked using the ``telemetry_services`` system. When defining a given skill requirement you must specify a ``type``. This ``type`` property must match a telemetry event thats has both a ``type`` and ``value`` field. The service will also generate events of it's own such as ``SkillActivated``\ , ``SkillDeactivated``\ , and ``SkillUnlocked``. This allows other skills to be used as requirements thereby making it possible to create rich, tree-like skill structures with multiple branching paths. Despite a slight delay in the processing time of events, by leveraging the telemetry system for the tracking of this progress it reduces the chance for cheating. It is also possible to post progress updates directly for a given skill if a real-time system is desired.

.. list-table::
   :header-rows: 1

   * - Member
     - Description
     - Type
     - Format / Schema
     - Default Value
     - Identifier
     - Unique
     - Required
   * - `uid <#uid>`_
     - The universally unique identifier of the object.
     - ``string``
     - uuid
     - ``uuid.v4()``
     - true
     - true
     - true
   * - `type <#type>`_
     - The unique identifier that will be used to match telemetry events.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `title <#title>`_
     - The textual title or name of the requirement.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `description <#description>`_
     - The textual description of the requirement.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `icon <#icon>`_
     - The icon to display for the requirement.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `value <#value>`_
     - The value that must be met in order for the requirement to be fulfilled.
     - ``object``
     - 
     - ``undefined``
     - false
     - false
     - true


ArchetypeDefinition
^^^^^^^^^^^^^^^^^^^

The archetype definition is a developer created concept that allows for the grouping of skills in order to create classifications of skill sets. The traditional use case for such a concept is to define a set of levels for all players, or to define player classes such as Mage, Warrior, Bard, and so on where each class has a different set of abilities from the other. Personas can have multiple archetypes associated with them and are possible to be enabled and disabled at will. An enabled archetype is one in which the persona should have access to use the skills defined within it. If a given skill hasn't been unlocked it, progress will be tracked accordingly. A disabled archetype will not gain any unlock progress but it will not lose existing progress either.

.. list-table::
   :header-rows: 1

   * - Member
     - Description
     - Type
     - Format / Schema
     - Default Value
     - Identifier
     - Unique
     - Required
   * - `uid <#uid>`_
     - The universally unique identifier of the object.
     - ``string``
     - uuid
     - ``uuid.v4()``
     - true
     - true
     - true
   * - `dateCreated <#dateCreated>`_
     - The date and time that the object was created.
     - ``string``
     - date-time
     - ``now()``
     - false
     - false
     - true
   * - `dateModified <#dateModified>`_
     - The date and time that the object was last updated.
     - ``string``
     - date-time
     - ``now()``
     - false
     - false
     - true
   * - `version <#version>`_
     - The optimistic locking version of the object.
     - ``integer``
     - 
     - ``0``
     - false
     - false
     - true
   * - `name <#name>`_
     - The unique name of the archetype.
     - ``string``
     - 
     - ``""``
     - true
     - true
     - true
   * - `title <#title>`_
     - A textual title or name of the archetype.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `description <#description>`_
     - A textual description of the archetype.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `icon <#icon>`_
     - The icon to display when representing the archetype.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `skills <#skills>`_
     - The list of all root skill uid's that define this archetype. A root skill is the first skill in a tree that has few to no requirements.
     - ``array``
     - 
     - ``
     - false
     - false
     - true
   * - `data <#data>`_
     - Stores any custom data to be used by the product.
     - ``object``
     - 
     - ``undefined``
     - false
     - false
     - true


Skill
^^^^^

The skill is the persona owned instance for a given skill definition and archetype. Since skills are linked to a specific archetype and persona it is possible to re-use skill definitions in multiple archetypes but maintain separate progress for each. The skill has an ``enabled`` status and an ``unlocked`` status that is used to indicate whether that skill is available and tracking progress or has been unlocked and can be used by the persona. When a given requirement has been met the ``complete`` flag is set to ``true`` to indicate that it's progress is finished. Once all requirement progresses have been marked ``complete`` then the ``unlocked`` flag is flipped to ``true`` automatically.

.. list-table::
   :header-rows: 1

   * - Member
     - Description
     - Type
     - Format / Schema
     - Default Value
     - Identifier
     - Unique
     - Required
   * - `uid <#uid>`_
     - The universally unique identifier of the object.
     - ``string``
     - uuid
     - ``uuid.v4()``
     - true
     - true
     - true
   * - `dateCreated <#dateCreated>`_
     - The date and time that the object was created.
     - ``string``
     - date-time
     - ``now()``
     - false
     - false
     - true
   * - `dateModified <#dateModified>`_
     - The date and time that the object was last updated.
     - ``string``
     - date-time
     - ``now()``
     - false
     - false
     - true
   * - `version <#version>`_
     - The optimistic locking version of the object.
     - ``integer``
     - 
     - ``0``
     - false
     - false
     - true
   * - `archetypeUid <#archetypeUid>`_
     - The unique identifier of the archetype associated with the persona and skill.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `skillUid <#skillUid>`_
     - The unique identifier of the skill being tracked.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `personaUid <#personaUid>`_
     - The unique identifier of the persona whose skill progress is being tracked.
     - ``string``
     - 
     - ``""``
     - false
     - false
     - true
   * - `enabled <#enabled>`_
     - Indicates if the skill is currently enabled and should be tracked if not already unlocked.
     - ``boolean``
     - 
     - ``true``
     - false
     - false
     - true
   * - `progress <#progress>`_
     - The persona's current progress for the given skill and archetype.
     - ``object``
     - 
     - ``undefined``
     - false
     - false
     - true
   * - `unlocked <#unlocked>`_
     - Indicates if the persona has unlocked and can begin the skill.
     - ``boolean``
     - 
     - ``false``
     - false
     - false
     - true
   * - `unlockProgress <#unlockProgress>`_
     - The persona's curent progress towards unlocking the skill.
     - ``array``
     - 
     - ``
     - false
     - false
     - true


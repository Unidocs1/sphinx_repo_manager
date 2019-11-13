---
title: "Concepts"
date: 2019-11-07T21:58:38.095Z
---

## Overview

This quest system provides a RESTful service for the management and tracking of player related progress of developer designed goals and rewards. The service composes three primary parts; the REST API that manages quest definitions and player progress, an event scraper and an event processor.

The REST API is used to define the definition of a given set of quests as well as the ability to retrieve a player's set of available quests and their progress.

The [`EventScraper`](scraper) is a background service used to retrieve telemetry events from the [`telemetry_services`](/docs/telemetry_services) system that is used by the [`EventProcessor`](processor). Events retrieved that are scraped are placed into a global redis queue which any instance of the service can process.

Once an event is placed in the global queue, the [`EventProcessor`](processor) pops it and begins processing the event. The processor first identifies all quests that reference the event type as a requirement and then uses it to update either the unlock progress or the primary progress of the quest for the given player.

## Data Structures

There are two primary data structures used in the quest system, `Quest` and `QuestDefinition`. The `QuestDefinition` is a class that designers use to create the structure of what a quest is and what is requirements are. The `Quest` is the class that tracks an individual player's progress for a particular `QuestDefinition`, including whether or not the player has unlocked it.

### Defining a Quest

To define a quest, a JSON object is `POST`ed to the `/quests` endpoint. The quest definition object has the following properties.

| Property                                                         | Description                                                                                                                           | Type      | Format / Schema | Default Value             | Identifier | Unique | Required |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------- | --------------- | ------------------------- | ---------- | ------ | -------- |
| [name](restapi/QuestDefinition#name)                             | The unique name of the quest.                                                                                                         | `string`  |                 | `""`                      | true       | true   | true     |
| [title](restapi/QuestDefinition#title)                           | A textual title or name of the quest.                                                                                                 | `string`  |                 | `""`                      | false      | false  | true     |
| [description](restapi/QuestDefinition#description)               | A textual description of the quest.                                                                                                   | `string`  |                 | `""`                      | false      | false  | true     |
| [icon](restapi/QuestDefinition#icon)                             | The icon to display when representing the quest.                                                                                      | `string`  |                 | `""`                      | false      | false  | true     |
| [entityUid](restapi/QuestDefinition#entityUid)                   | The universally unique identifier of the entity that gives out the quest.                                                             | `string`  |                 | `""`                      | false      | false  | true     |
| [requirements](restapi/QuestDefinition#requirements)             | The list of requirements that the persona must fulfill to complete the quest.                                                         | `array`   |                 | `` | false | false | true |
| [rewards](restapi/QuestDefinition#rewards)                       | The list of rewards that will be given once the quest has been completed.                                                             | `array`   |                 | `` | false | false | true |
| [dateAvailable](restapi/QuestDefinition#dateAvailable)           | The date and time that the quest will be first made available. A `null` value indicates immediately available.                        | `string`  | date-time       | `now()`                   | false      | false  | true     |
| [dateFinished](restapi/QuestDefinition#dateFinished)             | The date and time that the quest will no longer be available. A `null` value indicates no end date.                                   | `string`  | date-time       | `now()`                   | false      | false  | true     |
| [frequency](restapi/QuestDefinition#frequency)                   | The frequency that the quest can be repeated (e.g. 5m, 1h, 1w). A `null` value indicates that the quest cannot be repeated.           | `string`  |                 | `""`                      | false      | false  | true     |
| [unlockRequirements](restapi/QuestDefinition#unlockRequirements) | The list of requirements that the persona must meet to unlock the quest.                                                              | `array`   |                 | `` | false | false | true |
| [autostart](restapi/QuestDefinition#autostart)                   | Set to `true` to have quests automatically start tracking progress once unlocked, otherwise set to `false`. Default value is `false`. | `boolean` |                 | `false`                   | false      | false  | true     |
| [data](restapi/QuestDefinition#data)                             | Stores any custom data to be used by the product.                                                                                     | `object`  |                 | `undefined`               | false      | false  | true     |

### Autostart

The `autostart` property governs whether or not quest progress will begin to be tracked automatically following an `QuestUnlocked` event. This can be useful when establishing recurring quests (daily, weekly, holidays, etc) or subsequent quests in a series. If set to `true` the quest will be immediately started when a given player has met all unlock requirements. Optionally, the final event that unlocked the quest can be used in the actual progress as well when setting the `apply_event_on_autostart` service config option.

### Setting Requirements

All requirements, whether for main progress of unlocking, have the same structure.

| Member                                              | Description                                                              | Type     | Format / Schema | Default Value | Identifier | Unique | Required |
| --------------------------------------------------- | ------------------------------------------------------------------------ | -------- | --------------- | ------------- | ---------- | ------ | -------- |
| [type](restapi/QuestRequirement#type)               | The unique identifier that will be used to match telemetry events.       | `string` |                 | `""`          | false      | false  | true     |
| [title](restapi/QuestRequirement#title)             | The textual title or name of the requirement.                            | `string` |                 | `""`          | false      | false  | true     |
| [description](restapi/QuestRequirement#description) | The textual description of the requirement.                              | `string` |                 | `""`          | false      | false  | true     |
| [icon](restapi/QuestRequirement#icon)               | The icon to display for the quest.                                       | `string` |                 | `""`          | false      | false  | true     |
| [value](restapi/QuestRequirement#value)             | The value that must be met in order for the requirement to be fulfilled. | `any`    |                 | `undefined`   | false      | false  | true     |

The `type` property must match an existing telemetry event. As an example, if you want to have a quest complete after a player logs in you will set this to either `UserLogin` or `PersonaLogin`. If you wish to chain quests together you can specify `QuestComplete`.

The `title`, `description` and `icon` properties are used to render the requirement information to a client's display.

The `value` property can be any arbitrary type supported by JSON such as a `number`, `boolean`, `string` or even an `object`. In the event that a `number` value is specified, the system will compare progress using the less than (`<`) operator. This makes it possible to support use cases where multiple events can add up over time (such as player kills or item collection). Any other value type that is specified will be treated as a strict `==` comparison.

#### Unlock Requirements

A locked quest is one in which the player cannot start and track progress for. The `unlockRequirements` property contains the list of all requirements that must be met in order for the quest to be considered unlocked and available to the player. In addition, the `dateAvailable` and `dateFinished` properties are used to further gate the list of unlock requirements whereby the date set in `dateAvailable` must be reached for an unlock to be allowed but any attempt to start a request after the `dateFinished` will fail. This is valuable when it is desired to create quests for specific timed events, such as for holidays, anniversaries, etc.

#### Progress Requirements

Once a quest has been unlocked and started, the completion requirements are used when tracking progress. Quest completion requirements are specified in the `requirements` property. Only once the entire set of completion requirements has been met will a quest be considered complete.

### Defining Rewards

No quest system would be complete without rewards. Rewards are why players want to complete a given quest. Without it, there's little motivation for players to bother. Rewards in the system are loosely defined in order to make it possible to describe any number of desired outcomes. The structure for a reward is as follows.

| Member                                     | Description                                                            | Type                                     | Format / Schema | Default Value | Identifier | Unique | Required |
| ------------------------------------------ | ---------------------------------------------------------------------- | ---------------------------------------- | --------------- | ------------- | ---------- | ------ | -------- |
| [type](restapi/QuestReward#type)           | The type of reward that will be given.                                 | `` | | `PROGRESS` | false | false | true |
| [quantity](restapi/QuestReward#quantity)   | The quantity amount to reward.                                         | `number`                                 |                 | `0`           | false      | false  | true     |
| [entityUid](restapi/QuestReward#entityUid) | The universally unique identifier of the entity that will be rewarded. | `string`                                 |                 | `""`          | false      | false  | true     |

The `type` is an enum value that can one of the following: `ITEM`, `PROGRESS`, `QUEST`.

The `quantity` determines how much of a particular reward to give to the player.

Finally the `entityUid` is the globally unique identifier of the actual reward whether that's an item to be added to the player's inventory, progress made towards a skill or level or a new quest to start.

### Quest

The tracking of unlock and completion progress for a given quest and player is handled with the `Quest` class. This class has the following properties.

| Member                                               | Description                                                                 | Type      | Format / Schema | Default Value             | Identifier | Unique | Required |
| ---------------------------------------------------- | --------------------------------------------------------------------------- | --------- | --------------- | ------------------------- | ---------- | ------ | -------- |
| [questUid](restapi/Quest#questUid)                   | The unique identifier of the quest being tracked.                           | `string`  |                 | `""`                      | false      | false  | true     |
| [personaUid](restapi/Quest#personaUid)               | The unique identifier of the persona whose quest progress is being tracked. | `string`  |                 | `""`                      | false      | false  | true     |
| [progress](restapi/Quest#progress)                   | The persona's current progress for each of the quest requirements.          | `array`   |                 | `` | false | false | true |
| [completions](restapi/Quest#completions)             | The number of times that the quest has been completed by the persona.       | `number`  |                 | `0`                       | false      | false  | true     |
| [dateLastCompleted](restapi/Quest#dateLastCompleted) | The date and time that the persona last completed the quest.                | `string`  | date-time       | `now()`                   | false      | false  | true     |
| [dateLastStarted](restapi/Quest#dateLastStarted)     | The date and time that the persona last started the quest.                  | `string`  | date-time       | `now()`                   | false      | false  | true     |
| [unlocked](restapi/Quest#unlocked)                   | Indicates if the persona has unlocked and can begin the quest.              | `boolean` |                 | `false`                   | false      | false  | true     |
| [unlockProgress](restapi/Quest#unlockProgress)       | The persona's curent progress towards unlocking the quest.                  | `array`   |                 | `[]`                      | false      | false  | true     |

The `questUid` and `personaUid` are the unique identifiers of the quest definition being tracked for a given persona.

Quest completion progress is stored in the `progress` property. Once all requirements have been met and stored in this property the quest is considered to be complete.

The `completions` property contains the number of times that the persona has succcessfully completed the quest with the `dateLastCompleted` recording the date and time of the most recent completion.

The `dateLastStarted` indicates the date and time that the player began tracking completion progress of the quest. This will be `undefined` and cannot be set until the quest is `unlocked`.

When a player has unlocked a given quest the `unlocked` property will be set to `true`. If the quest's definition specifies `autostart` then `dateLastStarted` will also be set at the same time of the unlock.

The `unlockProgress` stores the tracked progress of whether or not the player has unlocked the quest. It has the same structure as the `progress` property.

#### Quest Progress

The quest progress is a very simple structure containing the following information.

| Member                                       | Description                                                   | Type     | Format / Schema | Default Value | Identifier | Unique | Required |
| -------------------------------------------- | ------------------------------------------------------------- | -------- | --------------- | ------------- | ---------- | ------ | -------- |
| [requirementUid](restapi/QuestProgress#type) | The unique identifier of the quest requirement being tracked. | `string` |                 | `""`          | false      | false  | true     |
| [value](restapi/QuestProgress#value)         | The current value of the player's progress.                   | `any`    |                 | `undefined`   | false      | false  | true     |

The `requirementUid` is the globally unique identifier of a specific requirement as defined in a given `QuestDefinition` object. It should be noted that two quest definitions with requirements referencing the same event will have different `uid` values. It is this `uid` value that is referenced here and must exactly match the defintion.

The `value` is the current value of the player's progress with the quest requirement. Its type is determined by the event data associated with the requirement. It is important that the value types match in order to be computed and compared correctly. `number` values will be incrementally added to the previous value, whereas any other value type will simply replace the previous value.

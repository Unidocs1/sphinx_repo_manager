---
title: "QuestDefinition"
date: 2019-11-07T21:58:38.095Z
---

Describes a single quest.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the quest. | `string` |  | `""` | true | true | true |
| [title](#title) | A textual title or name of the quest. | `string` |  | `""` | false | false | true |
| [description](#description) | A textual description of the quest. | `string` |  | `""` | false | false | true |
| [icon](#icon) | The icon to display when representing the quest. | `string` |  | `""` | false | false | true |
| [entityUid](#entityUid) | The universally unique identifier of the entity that gives out the quest. | `string` |  | `""` | false | false | true |
| [requirements](#requirements) | The list of requirements that the persona must fulfill to complete the quest. | `array` |  | `` | false | false | true |
| [rewards](#rewards) | The list of rewards that will be given once the quest has been completed. | `array` |  | `` | false | false | true |
| [dateAvailable](#dateAvailable) | The date and time that the quest will be first made available. A `null` value indicates immediately available. | `string` | date-time | `now()` | false | false | true |
| [dateFinished](#dateFinished) | The date and time that the quest will no longer be available. A `null` value indicates no end date. | `string` | date-time | `now()` | false | false | true |
| [frequency](#frequency) | The frequency that the quest can be repeated (e.g. 5m, 1h, 1w). A `null` value indicates that the quest cannot be repeated. | `string` |  | `""` | false | false | true |
| [unlockRequirements](#unlockRequirements) | The list of requirements that the persona must meet to unlock the quest. | `array` |  | `` | false | false | true |
| [autostart](#autostart) | Set to `true` to have quests automatically start tracking progress once unlocked, otherwise set to `false`. Default value is `false`. | `boolean` |  | `false` | false | false | true |
| [data](#data) | Stores any custom data to be used by the product. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "QuestRequirement"
    ],
    "rewards": [
        "QuestReward"
    ],
    "dateAvailable": "2019-11-07T21:58:38.180Z",
    "dateFinished": "2019-11-07T21:58:38.180Z",
    "frequency": "string",
    "unlockRequirements": [
        "QuestRequirement"
    ],
    "autostart": false
}
```

### Response

```json
{
    "uid": "b27a1260-66be-44c1-8f85-bf30bb74b36c",
    "dateCreated": "2019-11-07T21:58:38.180Z",
    "dateModified": "2019-11-07T21:58:38.180Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "entityUid": "string",
    "requirements": [
        "QuestRequirement"
    ],
    "rewards": [
        "QuestReward"
    ],
    "dateAvailable": "2019-11-07T21:58:38.180Z",
    "dateFinished": "2019-11-07T21:58:38.180Z",
    "frequency": "string",
    "unlockRequirements": [
        "QuestRequirement"
    ],
    "autostart": false
}
```


## Members

### uid

Type: `string`

Default Value: `uuid.v4()`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the object.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the object was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the object was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic locking version of the object.

### name

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The unique name of the quest.

### title

Type: `string`

Default Value: `""`

Required: `true`

A textual title or name of the quest.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the quest.

### icon

Type: `string`

Default Value: `""`

Required: `true`

The icon to display when representing the quest.

### entityUid

Type: `string`

Default Value: `""`

Required: `true`

The universally unique identifier of the entity that gives out the quest.

### requirements

Type: `array`

Default Value: ``

Required: `true`

The list of requirements that the persona must fulfill to complete the quest.

### rewards

Type: `array`

Default Value: ``

Required: `true`

The list of rewards that will be given once the quest has been completed.

### dateAvailable

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the quest will be first made available. A `null` value indicates immediately available.

### dateFinished

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the quest will no longer be available. A `null` value indicates no end date.

### frequency

Type: `string`

Default Value: `""`

Required: `true`

The frequency that the quest can be repeated (e.g. 5m, 1h, 1w). A `null` value indicates that the quest cannot be repeated.

### unlockRequirements

Type: `array`

Default Value: ``

Required: `true`

The list of requirements that the persona must meet to unlock the quest.

### autostart

Type: `boolean`

Default Value: `false`

Required: `true`

Set to `true` to have quests automatically start tracking progress once unlocked, otherwise set to `false`. Default value is `false`.

### data

Type: `object`

Default Value: `undefined`

Required: `true`

Stores any custom data to be used by the product.

## References

This data model is referenced in the following endpoints.

// TODO
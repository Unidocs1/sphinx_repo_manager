---
title: "Skill"
date: 2019-11-22T23:48:48.249Z
---

Tracks the progress of a specific skill for a given persona and archetype.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last updated. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [archetypeUid](#archetypeUid) | The unique identifier of the archetype associated with the persona and skill. | `string` |  | `""` | false | false | true |
| [skillUid](#skillUid) | The unique identifier of the skill being tracked. | `string` |  | `""` | false | false | true |
| [personaUid](#personaUid) | The unique identifier of the persona whose skill progress is being tracked. | `string` |  | `""` | false | false | true |
| [enabled](#enabled) | Indicates if the skill is currently enabled and should be tracked if not already unlocked. | `boolean` |  | `true` | false | false | true |
| [progress](#progress) | The persona's current progress for the given skill and archetype. | `object` |  | `undefined` | false | false | true |
| [unlocked](#unlocked) | Indicates if the persona has unlocked and can begin the skill. | `boolean` |  | `false` | false | false | true |
| [unlockProgress](#unlockProgress) | The persona's curent progress towards unlocking the skill. | `array` |  | `` | false | false | true |

## Examples
### Request

```json
{
    "enabled": false,
    "unlocked": false,
    "unlockProgress": [
        "SkillRequirementProgress"
    ]
}
```

### Response

```json
{
    "uid": "048fdceb-6f0a-41ad-a39f-2de197d6163a",
    "dateCreated": "2019-11-22T23:48:48.379Z",
    "dateModified": "2019-11-22T23:48:48.379Z",
    "version": 0,
    "archetypeUid": "string",
    "skillUid": "string",
    "personaUid": "string",
    "enabled": false,
    "unlocked": false,
    "unlockProgress": [
        "SkillRequirementProgress"
    ]
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

The date and time that the object was last updated.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic locking version of the object.

### archetypeUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the archetype associated with the persona and skill.

### skillUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the skill being tracked.

### personaUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the persona whose skill progress is being tracked.

### enabled

Type: `boolean`

Default Value: `true`

Required: `true`

Indicates if the skill is currently enabled and should be tracked if not already unlocked.

### progress

Type: `object`

Default Value: `undefined`

Required: `true`

The persona's current progress for the given skill and archetype.

### unlocked

Type: `boolean`

Default Value: `false`

Required: `true`

Indicates if the persona has unlocked and can begin the skill.

### unlockProgress

Type: `array`

Default Value: ``

Required: `true`

The persona's curent progress towards unlocking the skill.

## References

This data model is referenced in the following endpoints.

// TODO
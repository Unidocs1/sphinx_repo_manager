---
title: "Quest"
date: 2019-11-07T21:58:38.095Z
---

Tracks the progress of a specific quest for a given persona.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last updated. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [questUid](#questUid) | The unique identifier of the quest being tracked. | `string` |  | `""` | false | false | true |
| [personaUid](#personaUid) | The unique identifier of the persona whose quest progress is being tracked. | `string` |  | `""` | false | false | true |
| [progress](#progress) | The persona's current progress for each of the quest requirements. | `array` |  | `` | false | false | true |
| [completions](#completions) | The number of times that the quest has been completed by the persona. | `number` |  | `0` | false | false | true |
| [dateLastCompleted](#dateLastCompleted) | The date and time that the persona last completed the quest. | `string` | date-time | `now()` | false | false | true |
| [dateLastStarted](#dateLastStarted) | The date and time that the persona last started the quest. | `string` | date-time | `now()` | false | false | true |
| [unlocked](#unlocked) | Indicates if the persona has unlocked and can begin the quest. | `boolean` |  | `false` | false | false | true |
| [unlockProgress](#unlockProgress) | The persona's curent progress towards unlocking the quest. | `array` |  | `` | false | false | true |

## Examples
### Request

```json
{
    "progress": [
        "QuestProgress"
    ],
    "completions": 0,
    "dateLastCompleted": "2019-11-07T21:58:38.270Z",
    "dateLastStarted": "2019-11-07T21:58:38.270Z",
    "unlocked": false,
    "unlockProgress": [
        "QuestProgress"
    ]
}
```

### Response

```json
{
    "uid": "ab8627d8-cbde-4892-a410-d6ae60dec7db",
    "dateCreated": "2019-11-07T21:58:38.270Z",
    "dateModified": "2019-11-07T21:58:38.270Z",
    "version": 0,
    "questUid": "string",
    "personaUid": "string",
    "progress": [
        "QuestProgress"
    ],
    "completions": 0,
    "dateLastCompleted": "2019-11-07T21:58:38.270Z",
    "dateLastStarted": "2019-11-07T21:58:38.270Z",
    "unlocked": false,
    "unlockProgress": [
        "QuestProgress"
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

### questUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the quest being tracked.

### personaUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the persona whose quest progress is being tracked.

### progress

Type: `array`

Default Value: ``

Required: `true`

The persona's current progress for each of the quest requirements.

### completions

Type: `number`

Default Value: `0`

Required: `true`

The number of times that the quest has been completed by the persona.

### dateLastCompleted

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the persona last completed the quest.

### dateLastStarted

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the persona last started the quest.

### unlocked

Type: `boolean`

Default Value: `false`

Required: `true`

Indicates if the persona has unlocked and can begin the quest.

### unlockProgress

Type: `array`

Default Value: ``

Required: `true`

The persona's curent progress towards unlocking the quest.

## References

This data model is referenced in the following endpoints.

// TODO
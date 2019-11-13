---
title: "QuestRequirement"
date: 2019-11-07T21:58:38.095Z
---

Defines a single requirement that must be met to fulfill a quest.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [type](#type) | The unique identifier that will be used to match telemetry events. | `string` |  | `""` | false | false | true |
| [title](#title) | The textual title or name of the requirement. | `string` |  | `""` | false | false | true |
| [description](#description) | The textual description of the requirement. | `string` |  | `""` | false | false | true |
| [icon](#icon) | The icon to display for the quest. | `string` |  | `""` | false | false | true |
| [value](#value) | The value that must be met in order for the requirement to be fulfilled. | `number` |  | `0` | false | false | true |

## Examples
### Request

```json
{
    "type": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "value": 0
}
```

### Response

```json
{
    "uid": "d73be07e-3fe8-4815-a159-29d99cbc688f",
    "type": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "value": 0
}
```


## Members

### uid

Type: `string`

Default Value: `uuid.v4()`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the object.

### type

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier that will be used to match telemetry events.

### title

Type: `string`

Default Value: `""`

Required: `true`

The textual title or name of the requirement.

### description

Type: `string`

Default Value: `""`

Required: `true`

The textual description of the requirement.

### icon

Type: `string`

Default Value: `""`

Required: `true`

The icon to display for the quest.

### value

Type: `number`

Default Value: `0`

Required: `true`

The value that must be met in order for the requirement to be fulfilled.

## References

This data model is referenced in the following endpoints.

// TODO
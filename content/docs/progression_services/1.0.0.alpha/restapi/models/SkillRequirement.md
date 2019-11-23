---
title: "SkillRequirement"
date: 2019-11-22T23:48:48.249Z
---

Defines a single requirement that must be met to unlock a skill.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [type](#type) | The unique identifier that will be used to match telemetry events. | `string` |  | `""` | false | false | true |
| [title](#title) | The textual title or name of the requirement. | `string` |  | `""` | false | false | true |
| [description](#description) | The textual description of the requirement. | `string` |  | `""` | false | false | true |
| [icon](#icon) | The icon to display for the requirement. | `string` |  | `""` | false | false | true |
| [value](#value) | The value that must be met in order for the requirement to be fulfilled. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "type": "string",
    "title": "string",
    "description": "string",
    "icon": "string"
}
```

### Response

```json
{
    "uid": "7281cdf5-3b0c-4696-ba61-252a73622bfe",
    "type": "string",
    "title": "string",
    "description": "string",
    "icon": "string"
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

The icon to display for the requirement.

### value

Type: `object`

Default Value: `undefined`

Required: `true`

The value that must be met in order for the requirement to be fulfilled.

## References

This data model is referenced in the following endpoints.

// TODO
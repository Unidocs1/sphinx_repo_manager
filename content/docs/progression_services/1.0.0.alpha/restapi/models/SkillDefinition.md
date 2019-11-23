---
title: "SkillDefinition"
date: 2019-11-22T23:48:48.249Z
---

Describes a single trackable concept within the product that a persona can make progress towards and complete. A skill can be any talent, level, skill or other trackable concept.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the skill. | `string` |  | `""` | true | true | true |
| [title](#title) | A textual title or name of the skill. | `string` |  | `""` | false | false | true |
| [description](#description) | A textual description of the skill. | `string` |  | `""` | false | false | true |
| [icon](#icon) | The icon to display when representing the skill. | `string` |  | `""` | false | false | true |
| [requirements](#requirements) | The list of requirements that the persona must fulfill to unlock the skill. | `array` |  | `` | false | false | true |
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
        "SkillRequirement"
    ]
}
```

### Response

```json
{
    "uid": "07729916-a9ed-4582-aa29-89f183182ac5",
    "dateCreated": "2019-11-22T23:48:48.331Z",
    "dateModified": "2019-11-22T23:48:48.331Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "SkillRequirement"
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

The unique name of the skill.

### title

Type: `string`

Default Value: `""`

Required: `true`

A textual title or name of the skill.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the skill.

### icon

Type: `string`

Default Value: `""`

Required: `true`

The icon to display when representing the skill.

### requirements

Type: `array`

Default Value: ``

Required: `true`

The list of requirements that the persona must fulfill to unlock the skill.

### data

Type: `object`

Default Value: `undefined`

Required: `true`

Stores any custom data to be used by the product.

## References

This data model is referenced in the following endpoints.

// TODO
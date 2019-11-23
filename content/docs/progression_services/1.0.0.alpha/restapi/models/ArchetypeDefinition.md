---
title: "ArchetypeDefinition"
date: 2019-11-22T23:48:48.249Z
---

An archetype is a specific subset of one or more skill trees that a persona can elect to follow.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last updated. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the archetype. | `string` |  | `""` | true | true | true |
| [title](#title) | A textual title or name of the archetype. | `string` |  | `""` | false | false | true |
| [description](#description) | A textual description of the archetype. | `string` |  | `""` | false | false | true |
| [icon](#icon) | The icon to display when representing the archetype. | `string` |  | `""` | false | false | true |
| [skills](#skills) | The list of all root skill uid's that define this archetype. A root skill is the first skill in a tree that has few to no requirements. | `array` |  | `` | false | false | true |
| [data](#data) | Stores any custom data to be used by the product. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
    ]
}
```

### Response

```json
{
    "uid": "37377dc3-6b02-4ce6-9835-7c01e11e963a",
    "dateCreated": "2019-11-22T23:48:48.401Z",
    "dateModified": "2019-11-22T23:48:48.401Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
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

### name

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The unique name of the archetype.

### title

Type: `string`

Default Value: `""`

Required: `true`

A textual title or name of the archetype.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the archetype.

### icon

Type: `string`

Default Value: `""`

Required: `true`

The icon to display when representing the archetype.

### skills

Type: `array`

Default Value: ``

Required: `true`

The list of all root skill uid's that define this archetype. A root skill is the first skill in a tree that has few to no requirements.

### data

Type: `object`

Default Value: `undefined`

Required: `true`

Stores any custom data to be used by the product.

## References

This data model is referenced in the following endpoints.

// TODO
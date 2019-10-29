---
title: "AchievementDefinition"
date: 2019-10-29T00:13:51.965Z
---

Describes a single achievement that a user can unlock.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the achievement. | `string` |  | `""` | true | true | true |
| [description](#description) | A textual description of the achievement. | `string` |  | `""` | false | false | true |
| [badge](#badge) | The icon to display when representing the achievement. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "description": "string",
    "badge": "string"
}
```

### Response

```json
{
    "uid": "dfd936a4-62fa-4548-a7e8-7a7ba37fd8ae",
    "dateCreated": "2019-10-29T00:13:52.221Z",
    "dateModified": "2019-10-29T00:13:52.221Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "badge": "string"
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

The unique name of the achievement.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the achievement.

### badge

Type: `string`

Default Value: `""`

Required: `true`

The icon to display when representing the achievement.

## References

This data model is referenced in the following endpoints.

// TODO
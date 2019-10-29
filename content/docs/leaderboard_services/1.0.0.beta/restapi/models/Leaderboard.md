---
title: "Leaderboard"
date: 2019-10-28T17:42:16.105Z
---

Describes a single leaderboard.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the leaderboard. | `string` |  | `""` | true | true | true |
| [description](#description) | A textual description of the leaderboard. | `string` |  | `""` | false | false | true |
| [icon](#icon) | The icon to display when representing the leaderboard. | `string` |  | `""` | false | false | true |
| [compareFunc](#compareFunc) | The function to use when comparing two scores. The function must be of the form `function (score1:number, score2:number):bool`. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "description": "string",
    "icon": "string",
    "compareFunc": "string"
}
```

### Response

```json
{
    "uid": "0271f196-6513-4014-afd7-3171a2fcc619",
    "dateCreated": "2019-10-28T17:42:16.159Z",
    "dateModified": "2019-10-28T17:42:16.159Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "icon": "string",
    "compareFunc": "string"
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

The unique name of the leaderboard.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the leaderboard.

### icon

Type: `string`

Default Value: `""`

Required: `true`

The icon to display when representing the leaderboard.

### compareFunc

Type: `string`

Default Value: `""`

Required: `true`

The function to use when comparing two scores. The function must be of the form `function (score1:number, score2:number):bool`.

## References

This data model is referenced in the following endpoints.

// TODO
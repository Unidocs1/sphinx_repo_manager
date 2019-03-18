---
title: "Role"
date: 2019-03-18T05:50:55.822Z
chapter: true
---

Describes a collection of users that all have the same role. Roles are used to grant permissions.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the role. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the role was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the role was last updated. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the role. | `string` |  | `""` | true | true | true |
| [description](#description) | A textual description of the purpose of the role and its members. | `string` |  | `""` | false | false | true |
| [members](#members) | The list of UUIDs for each user that is a member of the role. | `array` | uuid | `` | false | false | true |
| [owners](#owners) | The list of UUIDs for each user that is an owner of the role. Owners can add and remove other users to and from the role. | `array` | uuid | `` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "description": "string",
    "members": [
        "string"
    ],
    "owners": [
        "string"
    ]
}
```

### Response

```json
{
    "uid": "477faa95-75e4-4b03-a46b-4d68960f601a",
    "dateCreated": "2019-03-18T05:50:55.951Z",
    "dateModified": "2019-03-18T05:50:55.951Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "members": [
        "string"
    ],
    "owners": [
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

The universally unique identifier of the role.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the role was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the role was last updated.

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

The unique name of the role.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the purpose of the role and its members.

### members

Type: `array`

Default Value: ``

Required: `true`

The list of UUIDs for each user that is a member of the role.

### owners

Type: `array`

Default Value: ``

Required: `true`

The list of UUIDs for each user that is an owner of the role. Owners can add and remove other users to and from the role.

## References

This data model is referenced in the following endpoints.

// TODO
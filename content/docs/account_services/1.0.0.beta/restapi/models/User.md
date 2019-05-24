---
title: "User"
date: 2019-05-24T20:08:59.489Z
---

Describes a single authorized user in the AcceleratXR ecosystem.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the user. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the user was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the user was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [name](#name) | The unique name of the user. | `string` |  | `""` | true | true | true |
| [email](#email) | The unique e-mail address of the user. | `string` | email | `""` | true | true | true |
| [firstName](#firstName) | The user's first name. | `string` |  | `""` | false | false | true |
| [lastName](#lastName) | The user's last name or surname. | `string` |  | `""` | false | false | true |
| [phone](#phone) | The user's telephone number. | `string` | phone | `""` | false | false | true |
| [roles](#roles) | The list of roles (by name) that the user is apart of and will assume privileges for. | `array` |  | `` | false | false | true |
| [externalIds](#externalIds) | The list of unique identifiers for each third-party platform the user is linked to. | `array` |  | `` | false | false | true |

## Examples
### Request

```json
{
    "name": "string",
    "email": "jsmith@gmail.com",
    "firstName": "string",
    "lastName": "string",
    "phone": "+1 (818) 867-5309",
    "roles": [
        "string"
    ],
    "externalIds": [
        "string"
    ]
}
```

### Response

```json
{
    "uid": "e3f91680-5462-471d-b7ff-ee2dbb199f2a",
    "dateCreated": "2019-05-24T20:09:00.212Z",
    "dateModified": "2019-05-24T20:09:00.212Z",
    "version": 0,
    "name": "string",
    "email": "jsmith@gmail.com",
    "firstName": "string",
    "lastName": "string",
    "phone": "+1 (818) 867-5309",
    "roles": [
        "string"
    ],
    "externalIds": [
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

The universally unique identifier of the user.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the user was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the user was last modified.

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

The unique name of the user.

### email

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The unique e-mail address of the user.

### firstName

Type: `string`

Default Value: `""`

Required: `true`

The user's first name.

### lastName

Type: `string`

Default Value: `""`

Required: `true`

The user's last name or surname.

### phone

Type: `string`

Default Value: `""`

Required: `true`

The user's telephone number.

### roles

Type: `array`

Default Value: ``

Required: `true`

The list of roles (by name) that the user is apart of and will assume privileges for.

### externalIds

Type: `array`

Default Value: ``

Required: `true`

The list of unique identifiers for each third-party platform the user is linked to.

## References

This data model is referenced in the following endpoints.

// TODO
---
title: "UserSecret"
date: 2019-03-18T23:07:13.099Z
---

Provides a single method of authentication for a given user. A user may have multiple secrets tied to their user account. This makes it possible to handle multiple types of authentication methods such as password, two-step authentication, pre-shared key and more.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the user secret. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the user secret was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the user secret was last updated. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [userId](#userId) | The universally unique identifier of the user account associated with the secret. | `string` | uuid | `""` | false | true | true |
| [type](#type) | The type of secret that is being stored. | `string` |  | `""` | false | false | true |
| [secret](#secret) | The underlying secret that is being stored. | `string` | password | `""` | false | false | true |

## Examples
### Request

```json
{
    "userId": "5281c670-30db-4b7f-84fe-bc43116251af",
    "type": "string",
    "secret": "string"
}
```

### Response

```json
{
    "uid": "aebc7fce-0491-43a4-9b6d-6eeeea223182",
    "dateCreated": "2019-03-18T23:07:13.242Z",
    "dateModified": "2019-03-18T23:07:13.242Z",
    "version": 0,
    "userId": "5281c670-30db-4b7f-84fe-bc43116251af",
    "type": "string",
    "secret": "string"
}
```


## Members

### uid

Type: `string`

Default Value: `uuid.v4()`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the user secret.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the user secret was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the user secret was last updated.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic locking version of the object.

### userId

Type: `string`

Default Value: `""`

Required: `true`

*Unique* The universally unique identifier of the user account associated with the secret.

### type

Type: `string`

Default Value: `""`

Required: `true`

The type of secret that is being stored.

### secret

Type: `string`

Default Value: `""`

Required: `true`

The underlying secret that is being stored.

## References

This data model is referenced in the following endpoints.

// TODO
---
title: "Profile"
date: 2019-07-05T22:50:13.161Z
---

An `Profile` is an object containing a user's specific social metadata and information. Each profile can have an alias name by which to identify the user other than their real name. A `data` property is provided to allow for an arbitrary storage of any metadata desired by the application. A `presence` property is also provided for storing the applications-specific current online state of the user.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The unique identifier of the user that the profile belongs to. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the profile was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the profile was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [alias](#alias) | The non-unique alternate name of the user. | `string` |  | `""` | false | false | true |
| [avatar](#avatar) | The URL, asset uid or other global identifier that references the user's avatar. | `string` |  | `""` | false | false | true |
| [data](#data) | An arbitrary map of key-value pairs containing the metadata of the profile. | `object` |  | `undefined` | false | false | true |
| [presence](#presence) | A string containing encoded data about a user's current online state. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

### Response

```json
{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.262Z",
    "dateModified": "2019-07-05T22:50:13.262Z",
    "version": 0,
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The unique identifier of the user that the profile belongs to.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the profile was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the profile was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic lock version.

### alias

Type: `string`

Default Value: `""`

Required: `true`

The non-unique alternate name of the user.

### avatar

Type: `string`

Default Value: `""`

Required: `true`

The URL, asset uid or other global identifier that references the user's avatar.

### data

Type: `object`

Default Value: `undefined`

Required: `true`

An arbitrary map of key-value pairs containing the metadata of the profile.

### presence

Type: `string`

Default Value: `""`

Required: `true`

A string containing encoded data about a user's current online state.

## References

This data model is referenced in the following endpoints.

// TODO
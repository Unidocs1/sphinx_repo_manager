---
title: "Persona"
date: 2019-05-24T20:03:52.354Z
---

An `Persona` is a unique persona of a user within the system. Users can have multiple personas per account and the persona can have associated data such as inventory, progress, achievements, etc.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the ticket. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the ticket was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the ticket was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [userUid](#userUid) | The unique identifier of the user that the persona belongs to. | `string` | uuid | `""` | false | false | true |
| [name](#name) | The unique name of the persona. | `string` |  | `""` | true | true | true |
| [description](#description) | A textual description of the persona. | `string` |  | `""` | false | false | true |
| [attributes](#attributes) | An arbitrary map of key-value pairs containing the characteristics of the persona. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{
    "name": "caskater",
    "description": "string",
    "attributes": {
        "location": "Space",
        "favoriteFood": "Sushi"
    }
}
```

### Response

```json
{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.724Z",
    "dateModified": "2019-05-24T20:03:52.724Z",
    "version": 0,
    "userUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "name": "caskater",
    "description": "string",
    "attributes": {
        "location": "Space",
        "favoriteFood": "Sushi"
    }
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the ticket.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the ticket was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the ticket was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic lock version.

### userUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that the persona belongs to.

### name

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The unique name of the persona.

### description

Type: `string`

Default Value: `""`

Required: `true`

A textual description of the persona.

### attributes

Type: `object`

Default Value: `undefined`

Required: `true`

An arbitrary map of key-value pairs containing the characteristics of the persona.

## References

This data model is referenced in the following endpoints.

// TODO
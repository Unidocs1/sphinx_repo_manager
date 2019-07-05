---
title: "UserLink"
date: 2019-07-05T22:50:13.161Z
---

The `UserLink` is a representation of a relationship from one user to another. Relatiopships have three potential states; `block`, `follow`, or `friend`. The `block` state describes a relationship to a user that the individual wishes not to encounter. The `follow` state describes a person whom the user wishes to encounter again in the future. The `friend` state describes a person that both users wish to encounter in the future. A `friend` link is automatically made when each user creates a `follow` link to each other.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the link. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the link was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the link was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [userUid](#userUid) | The unique identifier of the user that owns the link. | `string` | uuid | `""` | false | false | true |
| [otherUid](#otherUid) | The unique identifier of the other user the the link is for. | `string` | uuid | `""` | false | false | true |
| [status](#status) | The current state of the link. | `string` |  | `follow` | false | false | true |

## Examples
### Request

```json
{
    "status": "string"
}
```

### Response

```json
{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.309Z",
    "dateModified": "2019-07-05T22:50:13.309Z",
    "version": 0,
    "userUid": "2eac2651-e41f-45bf-8851-db717c3196bb",
    "otherUid": "4032b36f-e625-4e15-81bd-58edc5a4ed9f",
    "status": "string"
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the link.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the link was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the link was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic lock version.

### userUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that owns the link.

### otherUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the other user the the link is for.

### status

Type: `string`

Default Value: `follow`

Required: `true`

The current state of the link.

## References

This data model is referenced in the following endpoints.

// TODO
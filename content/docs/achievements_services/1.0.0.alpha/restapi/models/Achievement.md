---
title: "Achievement"
date: 2019-10-29T00:13:51.965Z
---

Describes a single achievement that a given user has already unlocked.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last updated. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [achievementUid](#achievementUid) | The unique identifier of the achievement that the user has unlocked. | `string` |  | `""` | false | false | true |
| [userUid](#userUid) | The unique identifier of the user that unlocked the achievement. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{}
```

### Response

```json
{
    "uid": "6d7d0e65-7460-4c32-9fe5-16248bd78bec",
    "dateCreated": "2019-10-29T00:13:52.288Z",
    "dateModified": "2019-10-29T00:13:52.288Z",
    "version": 0,
    "achievementUid": "string",
    "userUid": "string"
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

### achievementUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the achievement that the user has unlocked.

### userUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that unlocked the achievement.

## References

This data model is referenced in the following endpoints.

// TODO
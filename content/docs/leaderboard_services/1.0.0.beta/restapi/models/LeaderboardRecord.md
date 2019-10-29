---
title: "LeaderboardRecord"
date: 2019-10-28T17:42:16.105Z
---

Describes a user's single score record within a given leaderboard.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the object. | `string` | uuid | `uuid.v4()` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the object was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the object was last updated. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic locking version of the object. | `integer` |  | `0` | false | false | true |
| [leaderboardUid](#leaderboardUid) | The unique identifier of the leaderboard that the record belongs to. | `string` |  | `""` | false | false | true |
| [userUid](#userUid) | The unique identifier of the user that submitted the record. | `string` |  | `""` | false | false | true |
| [score](#score) | The user's leaderboard score that will be ranked. | `number` |  | `0` | false | false | true |

## Examples
### Request

```json
{
    "score": 0
}
```

### Response

```json
{
    "uid": "db28a581-b6c3-469a-b04a-65b13cd4d6a4",
    "dateCreated": "2019-10-28T17:42:16.180Z",
    "dateModified": "2019-10-28T17:42:16.180Z",
    "version": 0,
    "leaderboardUid": "string",
    "userUid": "string",
    "score": 0
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

### leaderboardUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the leaderboard that the record belongs to.

### userUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the user that submitted the record.

### score

Type: `number`

Default Value: `0`

Required: `true`

The user's leaderboard score that will be ranked.

## References

This data model is referenced in the following endpoints.

// TODO
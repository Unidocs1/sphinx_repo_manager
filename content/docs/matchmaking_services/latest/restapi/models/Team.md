---
title: "Team"
date: 2019-03-18T21:19:59.093Z
chapter: true
---

Describes a single team of players involved in a match.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [id](#id) | The index or unique identifier of the team. | `integer` |  | `0` | false | false | true |
| [members](#members) | The list of UUIDs for each user on the team. | `array` | uuid | `` | false | false | true |

## Examples
### Request

```json
{
    "members": [
        "string"
    ]
}
```

### Response

```json
{
    "id": 0,
    "members": [
        "string"
    ]
}
```


## Members

### id

Type: `integer`

Default Value: `0`

Required: `true`

The index or unique identifier of the team.

### members

Type: `array`

Default Value: ``

Required: `true`

The list of UUIDs for each user on the team.

## References

This data model is referenced in the following endpoints.

// TODO
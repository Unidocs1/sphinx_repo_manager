---
title: "Match"
date: 2019-03-18T21:19:59.093Z
chapter: true
---

Describes a group of players that have been successfully matched.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the match. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the match was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time tha tthe match was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [criteria](#criteria) | The list of criteria to use when filtering other tickets while searching for a match. | `array` |  | `` | false | false | true |
| [hostUid](#hostUid) | The UUID of the host user that made the match. | `string` | uuid | `""` | false | false | true |
| [numTeams](#numTeams) | The total number of teams represented in the match. | `number` |  | `0` | false | false | true |
| [serverUid](#serverUid) | The universally unique identifier of the session server associated with the match. | `string` | uuid | `""` | false | false | true |
| [teams](#teams) | The list of teams, containing player assignments, for the match. | `array` |  | `` | false | false | true |
| [teamSize](#teamSize) | The maximum number of players allowed per team. | `integer` |  | `0` | false | false | true |
| [users](#users) | The list of UUIDs for each user involved in the match. | `array` | uuid | `` | false | false | true |

## Examples
### Request

```json
{
    "criteria": [
        "Criteria"
    ],
    "numTeams": 0,
    "teams": [
        "Team"
    ],
    "teamSize": 0,
    "users": [
        "string"
    ]
}
```

### Response

```json
{
    "uid": "de2c087e-723b-4df9-9323-14d8d880f9b6",
    "dateCreated": "2019-03-18T21:19:59.251Z",
    "dateModified": "2019-03-18T21:19:59.251Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "55798941-57d7-40bf-aae1-85b5ceed0c2f",
    "numTeams": 0,
    "serverUid": "12c9f21e-eb28-4c53-8f0d-c47f5af6c31e",
    "teams": [
        "Team"
    ],
    "teamSize": 0,
    "users": [
        "string"
    ]
}
```


## Members

### uid

Type: `string`

Default Value: `""`

Required: `true`

*Unique* *Identifier*

The universally unique identifier of the match.

### dateCreated

Type: `string`

Default Value: `now()`

Required: `true`

The date and time that the match was created.

### dateModified

Type: `string`

Default Value: `now()`

Required: `true`

The date and time tha tthe match was last modified.

### version

Type: `integer`

Default Value: `0`

Required: `true`

The optimistic lock version.

### criteria

Type: `array`

Default Value: ``

Required: `true`

The list of criteria to use when filtering other tickets while searching for a match.

### hostUid

Type: `string`

Default Value: `""`

Required: `true`

The UUID of the host user that made the match.

### numTeams

Type: `number`

Default Value: `0`

Required: `true`

The total number of teams represented in the match.

### serverUid

Type: `string`

Default Value: `""`

Required: `true`

The universally unique identifier of the session server associated with the match.

### teams

Type: `array`

Default Value: ``

Required: `true`

The list of teams, containing player assignments, for the match.

### teamSize

Type: `integer`

Default Value: `0`

Required: `true`

The maximum number of players allowed per team.

### users

Type: `array`

Default Value: ``

Required: `true`

The list of UUIDs for each user involved in the match.

## References

This data model is referenced in the following endpoints.

// TODO
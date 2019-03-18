---
title: "Ticket"
date: 2019-03-18T21:19:59.093Z
chapter: true
---

Describes one or more users wishing to find another group of users to match against.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the ticket. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the ticket was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time that the ticket was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [criteria](#criteria) | The list of criteria to use when filtering other tickets while looking for a match. | `array` |  | `` | false | false | true |
| [hostUid](#hostUid) | The UUID of the user that is responsible for maintaining this ticket. | `string` | uuid | `""` | false | false | true |
| [matchUid](#matchUid) | The UUID of the match once matchmaking has completed successfully. | `string` | uuid | `""` | false | false | true |
| [minTeamSize](#minTeamSize) | The minimum number of users desired for any given team. | `number` |  | `0` | false | false | true |
| [maxTeamSize](#maxTeamSize) | The maximum number of users desired for any given team. | `number` |  | `0` | false | false | true |
| [numTeams](#numTeams) | The number of teams desired to be found. | `number` |  | `0` | false | false | true |
| [numUsers](#numUsers) | The number of users represented on the ticket. | `number` |  | `0` | false | false | true |
| [statistics](#statistics) | The list of statistics for all users represented on the ticket. | `array` |  | `` | false | false | true |
| [status](#status) | The current state of the ticket's processing. | `string` |  | `INITIALIZING` | false | false | true |
| [users](#users) | The list of UUIDs for each user represented on the ticket. | `array` | uuid | `` | false | false | true |

## Examples
### Request

```json
{
    "criteria": [
        "Criteria"
    ],
    "minTeamSize": 0,
    "maxTeamSize": 0,
    "numTeams": 0,
    "numUsers": 0,
    "statistics": [
        "Statistic"
    ],
    "status": "string",
    "users": [
        "string"
    ]
}
```

### Response

```json
{
    "uid": "37d0003e-a9e8-457f-a79b-ba1bab63c4b2",
    "dateCreated": "2019-03-18T21:19:59.302Z",
    "dateModified": "2019-03-18T21:19:59.302Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "29e468ec-e038-4b0b-a50d-3b23e5d66df5",
    "matchUid": "c5d4d41a-a6a5-4e93-ab4b-9edb166bdcb0",
    "minTeamSize": 0,
    "maxTeamSize": 0,
    "numTeams": 0,
    "numUsers": 0,
    "statistics": [
        "Statistic"
    ],
    "status": "string",
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

### criteria

Type: `array`

Default Value: ``

Required: `true`

The list of criteria to use when filtering other tickets while looking for a match.

### hostUid

Type: `string`

Default Value: `""`

Required: `true`

The UUID of the user that is responsible for maintaining this ticket.

### matchUid

Type: `string`

Default Value: `""`

Required: `true`

The UUID of the match once matchmaking has completed successfully.

### minTeamSize

Type: `number`

Default Value: `0`

Required: `true`

The minimum number of users desired for any given team.

### maxTeamSize

Type: `number`

Default Value: `0`

Required: `true`

The maximum number of users desired for any given team.

### numTeams

Type: `number`

Default Value: `0`

Required: `true`

The number of teams desired to be found.

### numUsers

Type: `number`

Default Value: `0`

Required: `true`

The number of users represented on the ticket.

### statistics

Type: `array`

Default Value: ``

Required: `true`

The list of statistics for all users represented on the ticket.

### status

Type: `string`

Default Value: `INITIALIZING`

Required: `true`

The current state of the ticket's processing.

### users

Type: `array`

Default Value: ``

Required: `true`

The list of UUIDs for each user represented on the ticket.

## References

This data model is referenced in the following endpoints.

// TODO
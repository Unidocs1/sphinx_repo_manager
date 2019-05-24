---
title: "Ticket"
date: 2019-05-24T20:04:07.747Z
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
| [teamSize](#teamSize) | The number of users desired for any given team. Can be represented as a number or a range using an object. | `object` |  | `undefined` | false | false | true |
| [numTeams](#numTeams) | The number of teams desired to be found. | `number` |  | `0` | false | false | true |
| [numUsers](#numUsers) | The number of users represented on the ticket. | `number` |  | `0` | false | false | true |
| [sessionUid](#sessionUid) | The UUID of the session once matchmaking has completed successfully. | `string` | uuid | `""` | false | false | true |
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
    "uid": "2c87f862-9e4b-49ae-a0d9-1b59366b2353",
    "dateCreated": "2019-05-24T20:04:08.269Z",
    "dateModified": "2019-05-24T20:04:08.269Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "ba955edd-135c-4a97-8127-7555c330d4a6",
    "numTeams": 0,
    "numUsers": 0,
    "sessionUid": "1b1bb947-7857-47c6-91e0-ffe4d9fda55b",
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

### teamSize

Type: `object`

Default Value: `undefined`

Required: `true`

The number of users desired for any given team. Can be represented as a number or a range using an object.

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

### sessionUid

Type: `string`

Default Value: `""`

Required: `true`

The UUID of the session once matchmaking has completed successfully.

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
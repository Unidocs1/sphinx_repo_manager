---
title: "Session"
date: 2019-05-24T20:04:17.193Z
---

A session is describes a real-time interaction between a group of one or more players.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [uid](#uid) | The universally unique identifier of the match. | `string` | uuid | `""` | true | true | true |
| [dateCreated](#dateCreated) | The date and time that the match was created. | `string` | date-time | `now()` | false | false | true |
| [dateModified](#dateModified) | The date and time tha tthe match was last modified. | `string` | date-time | `now()` | false | false | true |
| [version](#version) | The optimistic lock version. | `integer` |  | `0` | false | false | true |
| [data](#data) | The map of arbitrary data associated with the session. | `object` |  | `undefined` | false | false | true |
| [hostUid](#hostUid) | The UUID of the host user that owns the session. If no host is specified then the session is considered to be owned by the system itself. When a session has no host any member may modify the session data. If a host is specified then only that user may modify the session data. | `string` | uuid | `""` | false | false | true |
| [invited](#invited) | The list of UUIDs for each user that has been invited to the session by the host. | `array` | uuid | `` | false | false | true |
| [numTeams](#numTeams) | The total number of teams represented in the match. | `number` |  | `0` | false | false | true |
| [password](#password) | The secret password that must be given in order to join the session. | `string` |  | `""` | false | false | true |
| [serverUid](#serverUid) | The universally unique identifier of the session server associated with the match. | `string` | uuid | `""` | false | false | true |
| [status](#status) | The current activity state of the session. | `string` |  | `""` | false | false | true |
| [teams](#teams) | The list of teams, containing player assignments, for the match. | `array` |  | `` | false | false | true |
| [teamSize](#teamSize) | The maximum number of players allowed per team. | `integer` |  | `0` | false | false | true |
| [users](#users) | The list of UUIDs for each user involved in the match. | `array` | uuid | `` | false | false | true |
| [visibility](#visibility) | The visibility of the session within the global roster. | `string` |  | `""` | false | false | true |

## Examples
### Request

```json
{
    "invited": [
        "string"
    ],
    "numTeams": 0,
    "password": "string",
    "status": "string",
    "teams": [
        "Team"
    ],
    "teamSize": 0,
    "users": [
        "string"
    ],
    "visibility": "string"
}
```

### Response

```json
{
    "uid": "cda1d269-a9c9-4384-ba05-4aff28ea4c2d",
    "dateCreated": "2019-05-24T20:04:17.627Z",
    "dateModified": "2019-05-24T20:04:17.627Z",
    "version": 0,
    "hostUid": "ea564fc5-02fe-4c04-ad02-57599658848e",
    "invited": [
        "string"
    ],
    "numTeams": 0,
    "password": "string",
    "serverUid": "8321fb4d-645a-44d1-a661-447a7122d3f6",
    "status": "string",
    "teams": [
        "Team"
    ],
    "teamSize": 0,
    "users": [
        "string"
    ],
    "visibility": "string"
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

### data

Type: `object`

Default Value: `undefined`

Required: `true`

The map of arbitrary data associated with the session.

### hostUid

Type: `string`

Default Value: `""`

Required: `true`

The UUID of the host user that owns the session. If no host is specified then the session is considered to be owned by the system itself. When a session has no host any member may modify the session data. If a host is specified then only that user may modify the session data.

### invited

Type: `array`

Default Value: ``

Required: `true`

The list of UUIDs for each user that has been invited to the session by the host.

### numTeams

Type: `number`

Default Value: `0`

Required: `true`

The total number of teams represented in the match.

### password

Type: `string`

Default Value: `""`

Required: `true`

The secret password that must be given in order to join the session.

### serverUid

Type: `string`

Default Value: `""`

Required: `true`

The universally unique identifier of the session server associated with the match.

### status

Type: `string`

Default Value: `""`

Required: `true`

The current activity state of the session.

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

### visibility

Type: `string`

Default Value: `""`

Required: `true`

The visibility of the session within the global roster.

## References

This data model is referenced in the following endpoints.

// TODO
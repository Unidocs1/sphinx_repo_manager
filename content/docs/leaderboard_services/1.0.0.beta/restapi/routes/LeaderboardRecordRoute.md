---
title: "LeaderboardRecord Routes"
date: 2019-10-28T17:42:16.105Z
---



## Parameters
| Name       | Description                           |  Type |
| ---------- | ------------------------------------- | ----- |
|  |  |  |

## Routes

### FindAll
`GET /leaderboards/{id}/records`

Authentication: Optional

Returns all the records for a single leaderboard from the system that the user has access to based upon the given criteria.

#### Parameters
| Name       |
| ---------- |
| id |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /leaderboards/{id}/records
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /leaderboards/{id}/records`

Authentication: **Required**

Creates a new leaderboard record.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
POST /leaderboards/{id}/records
Content-Type: application/json
Authorization: jwt <token>

{
    "score": 0
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "46625acf-1b36-4c77-ad80-b4e632b06969",
    "dateCreated": "2019-10-28T17:42:16.189Z",
    "dateModified": "2019-10-28T17:42:16.189Z",
    "version": 0,
    "leaderboardUid": "string",
    "userUid": "string",
    "score": 0
}
```

### Truncate
`DELETE /leaderboards/{id}/records`

Authentication: **Required**

Deletes all the leaderboard's records from the service.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /leaderboards/{id}/records
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /leaderboards/{id}/records/count`

Authentication: Optional

Returns the count of records in a given leaderboard based on the given criteria.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /leaderboards/{id}/records/count
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "count": 0
}
```


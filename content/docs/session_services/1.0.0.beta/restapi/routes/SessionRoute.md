---
title: "Session Routes"
date: 2019-05-24T20:04:17.193Z
---



## Routes

### FindAll
`GET /sessions`

Authentication: **Required**

Returns all sessions from the system that the user has access to.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /sessions
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /sessions`

Authentication: **Required**

Create a new session.

#### Request
```http
POST /sessions
Content-Type: application/json
Authorization: jwt <token>

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

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "e10de325-cbb3-4c60-af00-499616632651",
    "dateCreated": "2019-05-24T20:04:17.723Z",
    "dateModified": "2019-05-24T20:04:17.723Z",
    "version": 0,
    "hostUid": "27b8abcd-01b2-456b-b248-2c69c96cea9b",
    "invited": [
        "string"
    ],
    "numTeams": 0,
    "password": "string",
    "serverUid": "46cee80a-412c-4be8-bf9f-f27f27e54918",
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

### Truncate
`DELETE /sessions`

Authentication: **Required**

Removes all sessions from the datastore.

#### Request
```http
DELETE /sessions
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /sessions/count`

Authentication: **Required**

Returns the count of sessions

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /sessions/count
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "count": 0
}
```

### FindById
`GET /sessions/{id}`

Authentication: **Required**

Returns a single session from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /sessions/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "e2166c0c-48ee-4486-99c4-306616590538",
    "dateCreated": "2019-05-24T20:04:17.725Z",
    "dateModified": "2019-05-24T20:04:17.725Z",
    "version": 0,
    "hostUid": "c228bc42-1417-4873-95fe-5074359aba47",
    "invited": [
        "string"
    ],
    "numTeams": 0,
    "password": "string",
    "serverUid": "4635462a-4eda-4f80-89e9-97748bd0e800",
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

### Update
`PUT /sessions/{id}`

Authentication: **Required**

Updates a single session

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /sessions/{id}
Content-Type: application/json
Authorization: jwt <token>

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

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "d66a724b-eb51-4b1f-98dc-950c0e88bebb",
    "dateCreated": "2019-05-24T20:04:17.727Z",
    "dateModified": "2019-05-24T20:04:17.727Z",
    "version": 0,
    "hostUid": "a4fd59c8-169b-4f86-b5bc-e320c005fab4",
    "invited": [
        "string"
    ],
    "numTeams": 0,
    "password": "string",
    "serverUid": "4fd2326a-1f5a-4d78-ad0d-fb98301a98b2",
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

### Delete
`DELETE /sessions/{id}`

Authentication: **Required**

Deletes the session

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /sessions/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Join
`GET /sessions/{id}/join`

Authentication: **Required**

Adds the authenticated user to the session with the specified identifier.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /sessions/{id}/join
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "5dae34ac-4280-461b-98bf-613c78b4f895",
    "dateCreated": "2019-05-24T20:04:17.729Z",
    "dateModified": "2019-05-24T20:04:17.729Z",
    "version": 0,
    "hostUid": "5cd1274f-5b47-4cba-b42d-7ef95a1a6000",
    "invited": [
        "string"
    ],
    "numTeams": 0,
    "password": "string",
    "serverUid": "52c69e80-2d94-4b1e-bd24-47ac82d40c3b",
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

### Leave
`GET /sessions/{id}/leave`

Authentication: **Required**

Removes the authenticated user from the session with the specified identifier.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /sessions/{id}/leave
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


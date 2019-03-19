---
title: "Ticket Routes"
date: 2019-03-18T23:09:30.967Z
---



## Routes

### FindAll
`GET /matchmaking/tickets`

Authentication: **Required**

Returns all tickets from the system that the user has access to.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /matchmaking/tickets
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /matchmaking/tickets`

Authentication: **Required**

Create a new ticket.

#### Request
```http
POST /matchmaking/tickets
Content-Type: application/json
Authorization: jwt <token>

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

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "cf1f404b-25b9-4e48-9d7f-7d67f255f7fc",
    "dateCreated": "2019-03-18T23:09:31.176Z",
    "dateModified": "2019-03-18T23:09:31.176Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "fef8ea75-9051-450b-ab1a-edeec6f6d5f3",
    "matchUid": "9ad3f9ad-c28c-49d9-ac50-02147043080d",
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

### Truncate
`DELETE /matchmaking/tickets`

Authentication: **Required**

Removes all tickets from the datastore.

#### Request
```http
DELETE /matchmaking/tickets
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /matchmaking/tickets/count`

Authentication: **Required**

Returns the count of tickets

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /matchmaking/tickets/count
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
`GET /matchmaking/tickets/{id}`

Authentication: **Required**

Returns a single ticket from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /matchmaking/tickets/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "79bd6316-e162-4363-b084-6fbda92c3234",
    "dateCreated": "2019-03-18T23:09:31.176Z",
    "dateModified": "2019-03-18T23:09:31.176Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "d8330e5d-5fa6-4f4c-be4c-cca869996477",
    "matchUid": "8b255ede-033d-4dd6-8b87-bc2dd56e3bc4",
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

### Update
`PUT /matchmaking/tickets/{id}`

Authentication: **Required**

Updates a single ticket

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /matchmaking/tickets/{id}
Content-Type: application/json
Authorization: jwt <token>

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

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "eb4331da-90b9-41a9-bd9a-5cf0dfaea438",
    "dateCreated": "2019-03-18T23:09:31.176Z",
    "dateModified": "2019-03-18T23:09:31.176Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "a8288c32-99c2-4a81-8f79-70dbc728c685",
    "matchUid": "914b48a3-aae6-4f1d-9d58-0ef760733097",
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

### Delete
`DELETE /matchmaking/tickets/{id}`

Authentication: **Required**

Deletes the ticket

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /matchmaking/tickets/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


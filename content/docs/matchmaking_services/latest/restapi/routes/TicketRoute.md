---
title: "Ticket Routes"
date: 2019-03-18T21:19:59.093Z
chapter: true
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
    "uid": "03b7a210-19f4-4c07-a42e-2baf6c5a4916",
    "dateCreated": "2019-03-18T21:19:59.317Z",
    "dateModified": "2019-03-18T21:19:59.317Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "1c7b16e7-04ba-4e84-8131-a90ed7b86d14",
    "matchUid": "28ae3889-bce6-403c-8f6c-f770e38c0569",
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
    "uid": "030956e5-e380-4140-a2c0-c25856e41b5b",
    "dateCreated": "2019-03-18T21:19:59.317Z",
    "dateModified": "2019-03-18T21:19:59.317Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "b45d59fe-d34b-431b-b9da-c016e1d84d23",
    "matchUid": "64196c93-359a-4f13-8420-15fffe4e6c45",
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
    "uid": "85478c15-c0da-4261-b2e6-622835d3d0f0",
    "dateCreated": "2019-03-18T21:19:59.318Z",
    "dateModified": "2019-03-18T21:19:59.318Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "c18e9cb0-f602-4c79-8988-7d02e4550ebf",
    "matchUid": "1b7296c5-7cfa-4dfb-85fa-4aed7e3f21da",
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


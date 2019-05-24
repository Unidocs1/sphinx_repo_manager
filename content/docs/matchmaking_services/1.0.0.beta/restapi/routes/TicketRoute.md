---
title: "Ticket Routes"
date: 2019-05-24T20:04:07.747Z
---



## Routes

### FindAll
`GET /tickets`

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
GET /tickets
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /tickets`

Authentication: **Required**

Create a new ticket.

#### Request
```http
POST /tickets
Content-Type: application/json
Authorization: jwt <token>

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

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9368158b-b521-4d82-926b-ce551dd5e3ce",
    "dateCreated": "2019-05-24T20:04:08.317Z",
    "dateModified": "2019-05-24T20:04:08.317Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "5714fbf7-9b61-4cb3-a36d-f69f53287b05",
    "numTeams": 0,
    "numUsers": 0,
    "sessionUid": "50bf7006-5fb0-4d43-b692-4f1e6b7c9c93",
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
`DELETE /tickets`

Authentication: **Required**

Removes all tickets from the datastore.

#### Request
```http
DELETE /tickets
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /tickets/count`

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
GET /tickets/count
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
`GET /tickets/{id}`

Authentication: **Required**

Returns a single ticket from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /tickets/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "93a189a7-d15e-4e20-9cfd-117100f256a5",
    "dateCreated": "2019-05-24T20:04:08.319Z",
    "dateModified": "2019-05-24T20:04:08.319Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "bc2ca40f-3899-4ae7-8532-da975679ee45",
    "numTeams": 0,
    "numUsers": 0,
    "sessionUid": "e5347e6a-c499-4d05-a027-01ff0a580c6a",
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
`PUT /tickets/{id}`

Authentication: **Required**

Updates a single ticket

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /tickets/{id}
Content-Type: application/json
Authorization: jwt <token>

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

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "db7d50a3-48fe-4af3-bb5b-7bb67b4683b7",
    "dateCreated": "2019-05-24T20:04:08.322Z",
    "dateModified": "2019-05-24T20:04:08.322Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "8a11e87c-6987-4ef2-b4ed-3a14983ccc79",
    "numTeams": 0,
    "numUsers": 0,
    "sessionUid": "70763b73-5c97-42ba-9def-198f150489f8",
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
`DELETE /tickets/{id}`

Authentication: **Required**

Deletes the ticket

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /tickets/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


---
title: "Snapshot Routes"
date: 2019-05-24T20:03:25.798Z
---



## Routes

### FindAll
`GET /snapshot`

Authentication: **Required**

Returns all snapshots from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /snapshot
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /snapshot`

Authentication: **Required**

Create a new snapshot

#### Request
```http
POST /snapshot
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "assets": [
        "string"
    ],
    "description": "string",
    "environment": "string",
    "notes": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "03b3a505-f3cf-4d32-88bd-8bc6a7f7b5c4",
    "dateCreated": "2019-05-24T20:03:30.573Z",
    "dateModified": "2019-05-24T20:03:30.573Z",
    "version": 0,
    "name": "string",
    "assets": [
        "string"
    ],
    "description": "string",
    "environment": "string",
    "notes": "string"
}
```

### Count
`GET /snapshot/count`

Authentication: **Required**

Returns the count of snapshots

#### Request
```http
GET /snapshot/count
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
`GET /snapshot/{id}`

Authentication: **Required**

Returns a single snapshot from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /snapshot/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "01a2dfad-4434-4937-afaa-ba04076e8027",
    "dateCreated": "2019-05-24T20:03:30.574Z",
    "dateModified": "2019-05-24T20:03:30.574Z",
    "version": 0,
    "name": "string",
    "assets": [
        "string"
    ],
    "description": "string",
    "environment": "string",
    "notes": "string"
}
```

### Delete
`DELETE /snapshot/{id}`

Authentication: **Required**

Deletes the file

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /snapshot/{id}
Authorization: jwt <token>
```

#### Response
```http
204 NO CONTENT
```

### FindDelta
`GET /snapshot/assets/{minimum}/{maximum}`

Authentication: **Required**

Returns the delta of assets in snapshots Minimum <= Name < Maximum

#### Parameters
| Name       |
| ---------- |
| minimum |

#### Parameters
| Name       |
| ---------- |
| maximum |

#### Request
```http
GET /snapshot/assets/{minimum}/{maximum}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```


---
title: "Role Routes"
date: 2019-03-18T21:15:14.179Z
chapter: true
---



## Routes

### FindAll
`GET /roles`

Authentication: Optional

Returns all groups from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /roles
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /roles`

Authentication: **Required**

Create a new group

#### Request
```http
POST /roles
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "description": "string",
    "members": [
        "string"
    ],
    "owners": [
        "string"
    ]
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "aaa35ebc-e9cf-430b-8b67-8e50106330e6",
    "dateCreated": "2019-03-18T21:15:14.322Z",
    "dateModified": "2019-03-18T21:15:14.322Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "members": [
        "string"
    ],
    "owners": [
        "string"
    ]
}
```

### Truncate
`DELETE /roles`

Authentication: **Required**

Deletes all roles from the service.

#### Request
```http
DELETE /roles
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /roles/count`

Authentication: Optional

Returns the count of groups

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /roles/count
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
`GET /roles/{id}`

Authentication: Optional

Returns a single group from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /roles/{id}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "a13773dd-605d-426e-9ffb-b5f73c7ee366",
    "dateCreated": "2019-03-18T21:15:14.322Z",
    "dateModified": "2019-03-18T21:15:14.322Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "members": [
        "string"
    ],
    "owners": [
        "string"
    ]
}
```

### Update
`PUT /roles/{id}`

Authentication: **Required**

Updates a single group

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /roles/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "description": "string",
    "members": [
        "string"
    ],
    "owners": [
        "string"
    ]
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "fdd2c2f8-c4ac-4e43-ae93-b11c5d53b259",
    "dateCreated": "2019-03-18T21:15:14.322Z",
    "dateModified": "2019-03-18T21:15:14.323Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "members": [
        "string"
    ],
    "owners": [
        "string"
    ]
}
```

### Delete
`DELETE /roles/{id}`

Authentication: **Required**

Deletes the group

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /roles/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


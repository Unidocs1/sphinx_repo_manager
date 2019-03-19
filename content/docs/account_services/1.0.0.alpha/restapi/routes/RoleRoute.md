---
title: "Role Routes"
date: 2019-03-18T23:07:13.099Z
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
    "uid": "183683c8-e100-4af4-a350-195a8db7d1e8",
    "dateCreated": "2019-03-18T23:07:13.258Z",
    "dateModified": "2019-03-18T23:07:13.258Z",
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
    "uid": "1cf31682-081c-4eca-a679-d898ba1c0fbe",
    "dateCreated": "2019-03-18T23:07:13.258Z",
    "dateModified": "2019-03-18T23:07:13.258Z",
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
    "uid": "e353430a-0c02-4146-9737-09dbc9d3713c",
    "dateCreated": "2019-03-18T23:07:13.258Z",
    "dateModified": "2019-03-18T23:07:13.258Z",
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


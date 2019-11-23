---
title: "ArchetypeDefinition Routes"
date: 2019-11-22T23:48:48.249Z
---



## Routes

### FindAll
`GET /archetypes`

Authentication: Optional

Returns all archetype definitions from the system that the persona has access to based upon the given criteria.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /archetypes
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /archetypes`

Authentication: **Required**

Creates a new archetype definition.

#### Request
```http
POST /archetypes
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
    ]
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "23eb1385-b0ab-46f0-b20d-b65fea653e0c",
    "dateCreated": "2019-11-22T23:48:48.413Z",
    "dateModified": "2019-11-22T23:48:48.413Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
    ]
}
```

### Truncate
`DELETE /archetypes`

Authentication: **Required**

Deletes all archetype definitions from the service.

#### Request
```http
DELETE /archetypes
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /archetypes/count`

Authentication: Optional

Returns the count of archetype definitions based on the given criteria.

#### Request
```http
GET /archetypes/count
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
`GET /archetypes/{id}`

Authentication: Optional

Returns a single archetype definition from the system that the persona has access to.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /archetypes/{id}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "e6eea42a-309f-444f-991f-a7aa55c05a93",
    "dateCreated": "2019-11-22T23:48:48.413Z",
    "dateModified": "2019-11-22T23:48:48.413Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
    ]
}
```

### Update
`PUT /archetypes/{id}`

Authentication: **Required**

Updates a single archetype definition.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /archetypes/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
    ]
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "4d3a2298-1dd7-458b-9ccb-44a301b568e0",
    "dateCreated": "2019-11-22T23:48:48.414Z",
    "dateModified": "2019-11-22T23:48:48.414Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "skills": [
        "string"
    ]
}
```

### Delete
`DELETE /archetypes/{id}`

Authentication: **Required**

Deletes the archetype from the service.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /archetypes/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


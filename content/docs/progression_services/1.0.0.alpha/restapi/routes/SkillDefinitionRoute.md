---
title: "SkillDefinition Routes"
date: 2019-11-22T23:48:48.249Z
---



## Routes

### FindAll
`GET /skills`

Authentication: Optional

Returns all skill definitions from the system that the persona has access to based upon the given criteria.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /skills
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /skills`

Authentication: **Required**

Creates a new skill definition.

#### Request
```http
POST /skills
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "SkillRequirement"
    ]
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "999a8c78-8903-4b7b-8c4b-57ae57d11ab7",
    "dateCreated": "2019-11-22T23:48:48.414Z",
    "dateModified": "2019-11-22T23:48:48.414Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "SkillRequirement"
    ]
}
```

### Truncate
`DELETE /skills`

Authentication: **Required**

Deletes all skill definitions from the service.

#### Request
```http
DELETE /skills
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /skills/count`

Authentication: Optional

Returns the count of skill definitions based on the given criteria.

#### Request
```http
GET /skills/count
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
`GET /skills/{id}`

Authentication: Optional

Returns a single skill definition from the system that the persona has access to.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /skills/{id}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "fa4a77b8-835c-40de-a068-b5cfcd1dbc34",
    "dateCreated": "2019-11-22T23:48:48.414Z",
    "dateModified": "2019-11-22T23:48:48.414Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "SkillRequirement"
    ]
}
```

### Update
`PUT /skills/{id}`

Authentication: **Required**

Updates a single skill definition.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /skills/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "SkillRequirement"
    ]
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "85cb28bb-0cb9-46e3-a554-d66722d3894f",
    "dateCreated": "2019-11-22T23:48:48.414Z",
    "dateModified": "2019-11-22T23:48:48.414Z",
    "version": 0,
    "name": "string",
    "title": "string",
    "description": "string",
    "icon": "string",
    "requirements": [
        "SkillRequirement"
    ]
}
```

### Delete
`DELETE /skills/{id}`

Authentication: **Required**

Deletes the skill from the service.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /skills/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


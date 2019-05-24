---
title: "PersonaStatDefinition Routes"
date: 2019-05-24T20:03:52.354Z
---



## Routes

### FindAll
`GET /personas/stats/definition`

Authentication: **Required**

Returns all persona stat definitions from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /personas/stats/definition
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /personas/stats/definition`

Authentication: **Required**

Create a persona stat definitions

#### Request
```http
POST /personas/stats/definition
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "type": "string",
    "default": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.861Z",
    "dateModified": "2019-05-24T20:03:52.861Z",
    "version": 0,
    "name": "string",
    "type": "string",
    "min": "string",
    "max": "string",
    "values": "string",
    "default": "string"
}
```

### Count
`GET /personas/stats/definition/count`

Authentication: **Required**

Returns the count of persona stat definitions

#### Request
```http
GET /personas/stats/definition/count
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
`GET /personas/stats/definition/{id}`

Authentication: **Required**

Returns a single persona stat definition from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /personas/stats/definition/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.862Z",
    "dateModified": "2019-05-24T20:03:52.862Z",
    "version": 0,
    "name": "string",
    "type": "string",
    "min": "string",
    "max": "string",
    "values": "string",
    "default": "string"
}
```

### Update
`PUT /personas/stats/definition/{id}`

Authentication: **Required**

Updates a single persona stat definition

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /personas/stats/definition/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "type": "string",
    "default": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.864Z",
    "dateModified": "2019-05-24T20:03:52.864Z",
    "version": 0,
    "name": "string",
    "type": "string",
    "min": "string",
    "max": "string",
    "values": "string",
    "default": "string"
}
```

### Delete
`DELETE /personas/stats/definition/{id}`

Authentication: **Required**

Deletes the persona stat definition

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /personas/stats/definition/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


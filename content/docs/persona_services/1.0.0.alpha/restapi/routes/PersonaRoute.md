---
title: "Persona Routes"
date: 2019-05-24T20:03:52.354Z
---



## Routes

### FindAll
`GET /personas`

Authentication: **Required**

Returns all personas from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /personas
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /personas`

Authentication: **Required**

Create a new persona.

#### Request
```http
POST /personas
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "caskater",
    "description": "string",
    "attributes": {
        "location": "Space",
        "favoriteFood": "Sushi"
    }
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.848Z",
    "dateModified": "2019-05-24T20:03:52.848Z",
    "version": 0,
    "userUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "name": "caskater",
    "description": "string",
    "attributes": {
        "location": "Space",
        "favoriteFood": "Sushi"
    }
}
```

### Count
`GET /personas/count`

Authentication: **Required**

Returns the count of personas

#### Request
```http
GET /personas/count
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
`GET /personas/{id}`

Authentication: **Required**

Returns a single persona from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /personas/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.849Z",
    "dateModified": "2019-05-24T20:03:52.849Z",
    "version": 0,
    "userUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "name": "caskater",
    "description": "string",
    "attributes": {
        "location": "Space",
        "favoriteFood": "Sushi"
    }
}
```

### Update
`PUT /personas/{id}`

Authentication: **Required**

Updates a single persona

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /personas/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "caskater",
    "description": "string",
    "attributes": {
        "location": "Space",
        "favoriteFood": "Sushi"
    }
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-05-24T20:03:52.851Z",
    "dateModified": "2019-05-24T20:03:52.851Z",
    "version": 0,
    "userUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "name": "caskater",
    "description": "string",
    "attributes": {
        "location": "Space",
        "favoriteFood": "Sushi"
    }
}
```

### Delete
`DELETE /personas/{id}`

Authentication: **Required**

Deletes the persona

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /personas/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


---
title: "AchievementDefinition Routes"
date: 2019-10-29T00:13:51.965Z
---



## Routes

### FindAll
`GET /achievements`

Authentication: **Required**

Returns all achievement definitions from the system that the user has access to based upon the given criteria.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /achievements
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /achievements`

Authentication: Optional

Creates a new achievement definition.

#### Request
```http
POST /achievements
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "badge": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "0aa9970e-1bfc-4531-a5ac-3911496ac4ea",
    "dateCreated": "2019-10-29T00:13:52.322Z",
    "dateModified": "2019-10-29T00:13:52.322Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "badge": "string"
}
```

### Truncate
`DELETE /achievements`

Authentication: **Required**

Deletes all achievement definitions from the service.

#### Request
```http
DELETE /achievements
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /achievements/count`

Authentication: Optional

Returns the count of achievement definitions based on the given criteria.

#### Request
```http
GET /achievements/count
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
`GET /achievements/{id}`

Authentication: **Required**

Returns a single achievement definition from the system that the user has access to.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /achievements/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "bcd21ad5-e5ab-4bd8-b4da-5b65c725443a",
    "dateCreated": "2019-10-29T00:13:52.322Z",
    "dateModified": "2019-10-29T00:13:52.322Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "badge": "string"
}
```

### Update
`PUT /achievements/{id}`

Authentication: **Required**

Updates a single achievement definition.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /achievements/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "description": "string",
    "badge": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "ecc077f3-6eec-435f-ba84-8534be556686",
    "dateCreated": "2019-10-29T00:13:52.323Z",
    "dateModified": "2019-10-29T00:13:52.323Z",
    "version": 0,
    "name": "string",
    "description": "string",
    "badge": "string"
}
```

### Delete
`DELETE /achievements/{id}`

Authentication: **Required**

Deletes the achievement definition from the service.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /achievements/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Unlock
`GET /achievements/{id}/unlock`

Authentication: **Required**

Unlocks the achievement with the given id for the authenticated user.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /achievements/{id}/unlock
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "0fe3a398-d248-4396-ba8f-dca161e42f8a",
    "dateCreated": "2019-10-29T00:13:52.323Z",
    "dateModified": "2019-10-29T00:13:52.323Z",
    "version": 0,
    "achievementUid": "string",
    "userUid": "string"
}
```


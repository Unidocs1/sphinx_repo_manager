---
title: "UserSecret Routes"
date: 2019-05-24T20:08:59.489Z
---



## Parameters
| Name       | Description                           |  Type |
| ---------- | ------------------------------------- | ----- |
|  |  |  |

## Routes

### FindAll
`GET /users/{userId}/secrets`

Authentication: **Required**

Returns all secrets for a given user.

#### Parameters
| Name       |
| ---------- |
| userId |

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /users/{userId}/secrets
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /users/{userId}/secrets`

Authentication: **Required**

Create a new user secret.

#### Parameters
| Name       |
| ---------- |
| userId |

#### Request
```http
POST /users/{userId}/secrets
Content-Type: application/json
Authorization: jwt <token>

{
    "userId": "86f4f074-e39d-4021-8a64-f14d543d8dbb",
    "type": "string",
    "secret": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "16fc3a93-ade4-48eb-9fae-35a1edd145c2",
    "dateCreated": "2019-05-24T20:09:00.535Z",
    "dateModified": "2019-05-24T20:09:00.535Z",
    "version": 0,
    "userId": "e373c080-71f7-427b-bf57-8b90b3198ead",
    "type": "string",
    "secret": "string"
}
```

### Count
`GET /users/{userId}/secrets/count`

Authentication: **Required**

Returns the count of UserSecret objects for a given user.

#### Parameters
| Name       |
| ---------- |
| userId |

#### Request
```http
GET /users/{userId}/secrets/count
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

### SetPassword
`GET /users/{userId}/secrets/password`

Authentication: **Required**

Sets the password for the user with the given unique identifier.

#### Parameters
| Name       |
| ---------- |
| userId |

#### Request
```http
GET /users/{userId}/secrets/password
Content-Type: application/json
Authorization: jwt <token>

{
    "userId": "d97846ee-7b44-4a91-935b-d75fc08ce733",
    "type": "string",
    "secret": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "e9ace2b0-3004-4c5f-a301-91d02789764b",
    "dateCreated": "2019-05-24T20:09:00.539Z",
    "dateModified": "2019-05-24T20:09:00.539Z",
    "version": 0,
    "userId": "3a6f5000-f74e-4d24-9817-ad19d641ae08",
    "type": "string",
    "secret": "string"
}
```

### FindById
`GET /users/{userId}/secrets/{id}`

Authentication: **Required**

Returns a single UserSecret for a specified user.

#### Parameters
| Name       |
| ---------- |
| userId |

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /users/{userId}/secrets/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "62438b78-74a1-433a-b471-f6d1967d85a5",
    "dateCreated": "2019-05-24T20:09:00.539Z",
    "dateModified": "2019-05-24T20:09:00.539Z",
    "version": 0,
    "userId": "789e9c42-009f-4805-b27a-82ca41099853",
    "type": "string",
    "secret": "string"
}
```

### Update
`PUT /users/{userId}/secrets/{id}`

Authentication: **Required**

Updates a single UserSecret

#### Parameters
| Name       |
| ---------- |
| userId |

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /users/{userId}/secrets/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "userId": "fffc495a-35ae-4f3e-a1c3-0be4c31c20a0",
    "type": "string",
    "secret": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "e47cfad8-cce6-4a58-9beb-d835a67e4a30",
    "dateCreated": "2019-05-24T20:09:00.541Z",
    "dateModified": "2019-05-24T20:09:00.541Z",
    "version": 0,
    "userId": "1fa7b5bd-72ce-4f95-aa8d-afcd396a689e",
    "type": "string",
    "secret": "string"
}
```

### Delete
`DELETE /users/{userId}/secrets/{id}`

Authentication: **Required**

Deletes the UserSecret

#### Parameters
| Name       |
| ---------- |
| userId |

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /users/{userId}/secrets/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


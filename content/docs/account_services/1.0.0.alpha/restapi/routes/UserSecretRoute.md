---
title: "UserSecret Routes"
date: 2019-03-18T23:07:13.099Z
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
    "userId": "3e0562de-f039-444e-bd85-867c96e5594d",
    "type": "string",
    "secret": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "52f18dc5-777d-41ff-a80a-ba412f5ed9d0",
    "dateCreated": "2019-03-18T23:07:13.258Z",
    "dateModified": "2019-03-18T23:07:13.259Z",
    "version": 0,
    "userId": "7e8071cb-7693-45e5-b4d8-fcb2c4bbd634",
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

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

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
    "uid": "f8023b70-9107-4b7e-91e5-b22551e6b745",
    "dateCreated": "2019-03-18T23:07:13.259Z",
    "dateModified": "2019-03-18T23:07:13.259Z",
    "version": 0,
    "userId": "2ac45044-e9d0-49b5-b9b2-8cf1cf88b723",
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
    "userId": "dea802ba-7b47-4576-9851-ae9a32ec3cbb",
    "type": "string",
    "secret": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "c58cb049-c0ba-49bc-a2e2-64e39745550a",
    "dateCreated": "2019-03-18T23:07:13.259Z",
    "dateModified": "2019-03-18T23:07:13.259Z",
    "version": 0,
    "userId": "b06d5c1a-008d-42a5-8eeb-6d38a10ed5b0",
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


---
title: "UserSecret Routes"
date: 2019-03-18T05:50:55.822Z
chapter: true
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
    "userId": "c31521e4-d719-4791-a55d-12793a793b0b",
    "type": "string",
    "secret": "string"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "27e267c3-4a8b-42f4-977d-12a3bc05ce84",
    "dateCreated": "2019-03-18T05:50:56.002Z",
    "dateModified": "2019-03-18T05:50:56.002Z",
    "version": 0,
    "userId": "f4e09130-82c4-4634-ab8f-9d6fd4f5cf37",
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
    "uid": "93db2b9f-7409-4368-bcff-da4287c896d9",
    "dateCreated": "2019-03-18T05:50:56.002Z",
    "dateModified": "2019-03-18T05:50:56.002Z",
    "version": 0,
    "userId": "5dc3125c-3116-40ea-a132-3cd842a08bd6",
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
    "userId": "7e8c4b0b-691e-43ad-934f-3d926411bc2c",
    "type": "string",
    "secret": "string"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "aefbee83-0af1-4932-ad53-1f997596e9c3",
    "dateCreated": "2019-03-18T05:50:56.002Z",
    "dateModified": "2019-03-18T05:50:56.002Z",
    "version": 0,
    "userId": "d71d23df-6673-4050-affe-cddefe6b0e72",
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


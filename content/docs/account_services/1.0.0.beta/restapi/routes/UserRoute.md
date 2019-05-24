---
title: "User Routes"
date: 2019-05-24T20:08:59.489Z
---



## Routes

### FindAll
`GET /users`

Authentication: **Required**

Returns all users from the system that the user has access to based upon the given criteria.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /users
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /users`

Authentication: Optional

Registers a new user to the service.

#### Request
```http
POST /users
Content-Type: application/json

{
    "name": "string",
    "email": "jsmith@gmail.com",
    "firstName": "string",
    "lastName": "string",
    "phone": "+1 (818) 867-5309",
    "roles": [
        "string"
    ],
    "externalIds": [
        "string"
    ]
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "token": "string"
}
```

### Truncate
`DELETE /users`

Authentication: **Required**

Deletes all users from the service.

#### Request
```http
DELETE /users
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /users/count`

Authentication: Optional

Returns the count of users based on the given criteria.

#### Request
```http
GET /users/count
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
`GET /users/{id}`

Authentication: **Required**

Returns a single user from the system that the user has access to.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /users/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "b48eca97-d07e-4065-8001-9d9f9b8be660",
    "dateCreated": "2019-05-24T20:09:00.524Z",
    "dateModified": "2019-05-24T20:09:00.524Z",
    "version": 0,
    "name": "string",
    "email": "jsmith@gmail.com",
    "firstName": "string",
    "lastName": "string",
    "phone": "+1 (818) 867-5309",
    "roles": [
        "string"
    ],
    "externalIds": [
        "string"
    ]
}
```

### Update
`PUT /users/{id}`

Authentication: **Required**

Updates a single user.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /users/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "string",
    "email": "jsmith@gmail.com",
    "firstName": "string",
    "lastName": "string",
    "phone": "+1 (818) 867-5309",
    "roles": [
        "string"
    ],
    "externalIds": [
        "string"
    ]
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "54e2cadb-1d75-44be-971f-4f38480cc278",
    "dateCreated": "2019-05-24T20:09:00.527Z",
    "dateModified": "2019-05-24T20:09:00.527Z",
    "version": 0,
    "name": "string",
    "email": "jsmith@gmail.com",
    "firstName": "string",
    "lastName": "string",
    "phone": "+1 (818) 867-5309",
    "roles": [
        "string"
    ],
    "externalIds": [
        "string"
    ]
}
```

### Delete
`DELETE /users/{id}`

Authentication: **Required**

Deletes the user from the service.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /users/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Recover
`GET /users/{id}/recover`

Authentication: Optional

Sends a temporary JWT token to the user's registered e-mail address allowing the password to be reset.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /users/{id}/recover
```

#### Response
```http
200 OK
```


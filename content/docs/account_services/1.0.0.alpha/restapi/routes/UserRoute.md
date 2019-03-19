---
title: "User Routes"
date: 2019-03-18T23:07:13.099Z
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

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

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

Authentication: Optional

Returns a single user from the system that the user has access to.

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /users/{id}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "0d75613e-4d02-45e3-ba00-b0ab2157ede0",
    "dateCreated": "2019-03-18T23:07:13.258Z",
    "dateModified": "2019-03-18T23:07:13.258Z",
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
    "uid": "3b5de5a1-dbb7-4f03-9a9e-fc42d77fecaa",
    "dateCreated": "2019-03-18T23:07:13.258Z",
    "dateModified": "2019-03-18T23:07:13.258Z",
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


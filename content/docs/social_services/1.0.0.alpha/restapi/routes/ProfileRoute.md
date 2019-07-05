---
title: "Profile Routes"
date: 2019-07-05T22:50:13.161Z
---



## Routes

### FindAll
`GET /profiles`

Authentication: **Required**

Returns all profiles from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /profiles
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /profiles`

Authentication: **Required**

Create a new profile.

#### Request
```http
POST /profiles
Content-Type: application/json
Authorization: jwt <token>

{
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.326Z",
    "dateModified": "2019-07-05T22:50:13.326Z",
    "version": 0,
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

### Count
`GET /profiles/count`

Authentication: **Required**

Returns the count of profiles

#### Request
```http
GET /profiles/count
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
`GET /profiles/{id}`

Authentication: **Required**

Returns a single profile from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /profiles/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.326Z",
    "dateModified": "2019-07-05T22:50:13.326Z",
    "version": 0,
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

### Update
`PUT /profiles/{id}`

Authentication: **Required**

Updates a single profile

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /profiles/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.326Z",
    "dateModified": "2019-07-05T22:50:13.326Z",
    "version": 0,
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

### Delete
`DELETE /profiles/{id}`

Authentication: **Required**

Deletes the profile

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /profiles/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### FindByUserUid
`GET /{userUid}/profile`

Authentication: **Required**

Returns the profile from the system for the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
GET /{userUid}/profile
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.326Z",
    "dateModified": "2019-07-05T22:50:13.326Z",
    "version": 0,
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

### UpdateByUserUid
`PUT /{userUid}/profile`

Authentication: **Required**

Creates or updates the profile for the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
PUT /{userUid}/profile
Content-Type: application/json
Authorization: jwt <token>

{
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "dateCreated": "2019-07-05T22:50:13.326Z",
    "dateModified": "2019-07-05T22:50:13.326Z",
    "version": 0,
    "alias": "acceleratxr",
    "avatar": "https://en.gravatar.com/acceleratxr 9c638e52-7dbe-4f11-97a9-648da49138bf",
    "data": {
        "twitter": "acceleratxr",
        "bio": "This is my biography.",
        "location": "Los Angeles, CA, USA"
    },
    "presence": "ONLINE"
}
```

### DeleteByUserUid
`DELETE /{userUid}/profile`

Authentication: **Required**

Deletes the profile for the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
DELETE /{userUid}/profile
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### GetUserPresence
`GET /{userUid}/profile/presence`

Authentication: **Required**

Returns the profile presence data for the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
GET /{userUid}/profile/presence
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### SetUserPresence
`PUT /{userUid}/profile/presence`

Authentication: **Required**

Sets the profile presence data for the given user.

#### Parameters
| Name       |
| ---------- |
| userUid |

#### Request
```http
PUT /{userUid}/profile/presence
Content-Type: application/json
Authorization: jwt <token>

{}
```

#### Response
```http
204 NO CONTENT
```


---
title: "Match Routes"
date: 2019-03-18T21:19:59.093Z
chapter: true
---



## Routes

### FindAll
`GET /matchmaking/matches`

Authentication: **Required**

Returns all matches from the system that the user has access to

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /matchmaking/matches
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Truncate
`DELETE /matchmaking/matches`

Authentication: **Required**

Removes all matches from the datastore.

#### Request
```http
DELETE /matchmaking/matches
Authorization: jwt <token>
```

#### Response
```http
200 OK
```

### Count
`GET /matchmaking/matches/count`

Authentication: **Required**

Returns the count of matches

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /matchmaking/matches/count
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
`GET /matchmaking/matches/{id}`

Authentication: **Required**

Returns a single match from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /matchmaking/matches/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "33b67789-7783-4b3c-88a8-46554e228d13",
    "dateCreated": "2019-03-18T21:19:59.319Z",
    "dateModified": "2019-03-18T21:19:59.319Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "71641c65-0080-4ed1-aa66-31b7cb052093",
    "numTeams": 0,
    "serverUid": "811557d9-ecdf-4685-b4ce-5e737d0f4def",
    "teams": [
        "Team"
    ],
    "teamSize": 0,
    "users": [
        "string"
    ]
}
```

### Update
`PUT /matchmaking/matches/{id}`

Authentication: **Required**

Updates a single match

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /matchmaking/matches/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "criteria": [
        "Criteria"
    ],
    "numTeams": 0,
    "teams": [
        "Team"
    ],
    "teamSize": 0,
    "users": [
        "string"
    ]
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "f896b780-c6e0-429f-80cf-ca6212db8098",
    "dateCreated": "2019-03-18T21:19:59.320Z",
    "dateModified": "2019-03-18T21:19:59.320Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "507b7f12-d828-400f-a9fd-bf4b63b4556b",
    "numTeams": 0,
    "serverUid": "98e66366-042c-4f46-b10a-8f17d8079628",
    "teams": [
        "Team"
    ],
    "teamSize": 0,
    "users": [
        "string"
    ]
}
```

### Delete
`DELETE /matchmaking/matches/{id}`

Authentication: **Required**

Deletes the match

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /matchmaking/matches/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


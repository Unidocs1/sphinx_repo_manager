---
title: "Match Routes"
date: 2019-03-18T23:09:30.967Z
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
    "uid": "4db66d7d-15b9-4315-aa41-2f81fcfe4768",
    "dateCreated": "2019-03-18T23:09:31.176Z",
    "dateModified": "2019-03-18T23:09:31.176Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "86bec472-9012-4bcd-9302-adc58113683f",
    "numTeams": 0,
    "serverUid": "a7d4dd8e-4a12-45d3-a1b4-bcf15813dcf8",
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
    "uid": "d3130eb0-e5a8-4c7e-a116-609f3773320c",
    "dateCreated": "2019-03-18T23:09:31.176Z",
    "dateModified": "2019-03-18T23:09:31.176Z",
    "version": 0,
    "criteria": [
        "Criteria"
    ],
    "hostUid": "5b4d9792-60dc-46c1-8cff-4473a56290ed",
    "numTeams": 0,
    "serverUid": "2127f38e-26db-4eed-94c9-d7c64cd4ecb1",
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


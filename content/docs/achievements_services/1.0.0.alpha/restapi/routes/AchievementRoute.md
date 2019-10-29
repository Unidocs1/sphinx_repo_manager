---
title: "Achievement Routes"
date: 2019-10-29T00:13:51.965Z
---



## Parameters
| Name       | Description                           |  Type |
| ---------- | ------------------------------------- | ----- |
|  |  |  |

## Routes

### FindAll
`GET /users/{userId}/achievements`

Authentication: **Required**

Returns all achievements that the given user has unlocked.

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
GET /users/{userId}/achievements
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Count
`GET /users/{userId}/achievements/count`

Authentication: **Required**

Returns the count of Achievement objects that a given user has unlocked.

#### Parameters
| Name       |
| ---------- |
| userId |

#### Request
```http
GET /users/{userId}/achievements/count
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


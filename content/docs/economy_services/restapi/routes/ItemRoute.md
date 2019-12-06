---
title: "Item Routes"
date: 2019-12-06T19:01:21.222Z
---



## Routes

### FindAll
`GET /items`

Authentication: **Required**

Returns all items from the system that the user has access to.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /items
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Create
`POST /items`

Authentication: **Required**

Create a new item.

#### Request
```http
POST /items
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "Pew Pew Gun",
    "description": "string",
    "cost": 0,
    "stats": [
        "Stat"
    ],
    "assetId": "string",
    "iconAssetId": "892792ed-02a2-4ca9-9651-7c77ddc25194",
    "parentUID": "4e7a45cd-a3a4-4083-9487-78307be36ca8"
}
```

#### Response
```http
201 CREATED
Content-Type: application/json

{
    "uid": "6368a216-90ba-4be0-955f-1880002033d2",
    "dateCreated": "2019-12-06T19:01:21.575Z",
    "dateModified": "2019-12-06T19:01:21.575Z",
    "version": 0,
    "name": "Pew Pew Gun",
    "description": "string",
    "cost": 0,
    "stats": [
        "Stat"
    ],
    "assetId": "string",
    "iconAssetId": "083bae2a-8615-46bb-83e3-088454430d56",
    "parentUID": "ea3010fe-561d-4746-b317-28fd28ea92e7"
}
```

### Count
`GET /items/count`

Authentication: **Required**

Returns the count of items

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /items/count
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
`GET /items/{id}`

Authentication: **Required**

Returns a single item from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /items/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "bca09b70-caae-4b13-ad45-4a531ae89c63",
    "dateCreated": "2019-12-06T19:01:21.575Z",
    "dateModified": "2019-12-06T19:01:21.575Z",
    "version": 0,
    "name": "Pew Pew Gun",
    "description": "string",
    "cost": 0,
    "stats": [
        "Stat"
    ],
    "assetId": "string",
    "iconAssetId": "b03a7366-a335-4e75-bdb9-595de2e9eba7",
    "parentUID": "dfa92fd9-04e7-4fc2-80b0-ffb5e5e41ae3"
}
```

### Update
`PUT /items/{id}`

Authentication: **Required**

Updates a single item

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
PUT /items/{id}
Content-Type: application/json
Authorization: jwt <token>

{
    "name": "Pew Pew Gun",
    "description": "string",
    "cost": 0,
    "stats": [
        "Stat"
    ],
    "assetId": "string",
    "iconAssetId": "9d942b03-86bc-4aac-8a92-711a67c0b17e",
    "parentUID": "f8a80b37-f989-414a-8a11-9ce7edc64115"
}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "7f1a5393-41b2-405c-9c8d-6ea088f9d04d",
    "dateCreated": "2019-12-06T19:01:21.576Z",
    "dateModified": "2019-12-06T19:01:21.576Z",
    "version": 0,
    "name": "Pew Pew Gun",
    "description": "string",
    "cost": 0,
    "stats": [
        "Stat"
    ],
    "assetId": "string",
    "iconAssetId": "3aba63b4-132b-4f86-b7f8-30f2916ee6e3",
    "parentUID": "9e04b271-6032-4431-9906-9c22b3a731ef"
}
```

### Delete
`DELETE /items/{id}`

Authentication: **Required**

Deletes the item

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
DELETE /items/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
```


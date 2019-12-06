---
title: "InventoryItem Routes"
date: 2019-12-06T19:01:21.222Z
---



## Routes

### FindAll
`GET /inventories`

Authentication: **Required**

Returns all inventories from the system that the user has access to.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /inventories
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Count
`GET /inventories/count`

Authentication: **Required**

Returns the count of inventories item

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /inventories/count
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
`GET /inventories/{id}`

Authentication: **Required**

Returns a single inventory item from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /inventories/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "52bb6a21-ef6f-42d8-baa5-d1a5ea5cb3a8",
    "dateCreated": "2019-12-06T19:01:21.576Z",
    "dateModified": "2019-12-06T19:01:21.576Z",
    "version": 0,
    "personaUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "itemUid": "8a3925f3-fe93-4546-8050-cac6f7f69910",
    "quantity": 0
}
```

### CreateTransaction
`POST /inventories/transaction`

Authentication: **Required**

Creates and processes a transaction on inventories

#### Request
```http
POST /inventories/transaction
Content-Type: application/json
Authorization: jwt <token>

{}
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "7fc666c5-34a1-4586-bf98-032ec7a7a1ea",
    "dateCreated": "2019-12-06T19:01:21.576Z",
    "dateModified": "2019-12-06T19:01:21.576Z",
    "version": 0,
    "status": "string",
    "type": "string",
    "personaOneUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "personaTwoUid": "9ff78212-8447-4cd6-b100-9791d7e9d47b",
    "personaOneInventoryItemsBefore": [
        "InventoryItem"
    ],
    "personaOneInventoryItemsAfter": [
        "InventoryItem"
    ],
    "personaTwoInventoryItemsBefore": [
        "InventoryItem"
    ],
    "personaTwoInventoryItemsAfter": [
        "InventoryItem"
    ]
}
```


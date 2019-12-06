---
title: "Transaction Routes"
date: 2019-12-06T19:01:21.222Z
---



## Routes

### FindAll
`GET /transactions`

Authentication: **Required**

Returns all transactions from the system that the user has access to.

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /transactions
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{}
```

### Count
`GET /transactions/count`

Authentication: **Required**

Returns the count of transactions

#### Query
| Name       | Description | Type | Default Value |
| ---------- | ---------------------------------------------------------------- | ------ | ------------- |
| limit      | The maximimum number of results to return. Cannot exceed `1000`. | number | 100           |
| skip       | The number of items to skip in the results (pagination).         | number | 0             |
| sort       | An object containing the name of the member to sort by and the order in which to sort. | object | `{ member: "<ASC|DESC>" } |

#### Request
```http
GET /transactions/count
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
`GET /transactions/{id}`

Authentication: **Required**

Returns a single transaction from the system that the user has access to

#### Parameters
| Name       |
| ---------- |
| id |

#### Request
```http
GET /transactions/{id}
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "uid": "fe968f16-0050-4127-8e0c-eba0b5821f55",
    "dateCreated": "2019-12-06T19:01:21.577Z",
    "dateModified": "2019-12-06T19:01:21.577Z",
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


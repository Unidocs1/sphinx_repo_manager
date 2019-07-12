---
title: "Validate Routes"
date: 2019-07-12T00:24:32.539Z
---



## Routes

### ValidateGoogle
`POST /validate/google`

Authentication: **Required**

Validates an in-app purchase with the Google Play store.

#### Request
```http
POST /validate/google
Content-Type: application/json
Authorization: jwt <token>

{
    "packageName": "string",
    "productId": "string",
    "token": "string",
    "type": "string"
}
```

#### Response
```http
200 OK
```

### ValidateApple
`POST /validate/apple`

Authentication: **Required**

Validates an in-app purchase with the Apple Store.

#### Request
```http
POST /validate/apple
Content-Type: application/json
Authorization: jwt <token>

{
    "receipt": "string"
}
```

#### Response
```http
200 OK
```


---
title: "AuthBasic Routes"
date: 2019-05-24T20:08:59.489Z
---



## Routes

### Authenticate
`GET /auth/password`

Authentication: **Required**

Authenticates the user using HTTP Basic and returns a JSON Web Token access token to be used with future API requests.

#### Request
```http
GET /auth/password
Authorization: jwt <token>
```

#### Response
```http
200 OK
Content-Type: application/json

{
    "token": "string"
}
```


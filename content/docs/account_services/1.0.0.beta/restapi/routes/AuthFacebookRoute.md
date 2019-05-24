---
title: "AuthFacebook Routes"
date: 2019-05-24T20:08:59.489Z
---



## Routes

### Authenticate
`GET /auth/facebook`

Authentication: **Required**

Authenticates the user using a provided Facebook access token and returns a JSON Web Token access token to be used with future API requests.

#### Request
```http
GET /auth/facebook
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


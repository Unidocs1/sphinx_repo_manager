---
title: "AuthFacebook Routes"
date: 2019-03-18T23:07:13.099Z
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


---
title: "Security"
date: 2019-03-18T16:34:43-07:00
weight: 2
---

In order to provide a common system for authentication [JSON Web Token (JWT)](http://jwt.io) access tokens are used in order to establish the identity and privileges of a user within the system. By default, all services automatically authenticate clients that provide a JWT token in the request. If a user has been properly identified you can add a `@User` decorated argument to any route handler to inject the authenticated user object.

The `user` object as passed in to each route handler will have the following fields.

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Description</th>
            <th>Default Value</th>
            <th>Required</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>`uid`</td>
            <td>`UUID`</td>
            <td>The universally unique identifier (UUID) of the user</td>
            <td></td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>`name`</td>
            <td>`string`</td>
            <td>The unique identifying name of the user.</td>
            <td></td>
            <td>No</td>
        </tr>
        <tr>
            <td>`email`</td>
            <td>`string`</td>
            <td>The e-mail address that is registered to the user account. Check the verified property to ensure that the e-mail has been verified as valid.</td>
            <td></td>
            <td>No</td>
        </tr>
        <tr>
            <td>`roles`</td>
            <td>`array[string]`</td>
            <td>An array of unique roles names indicating the privileges that the user has</td>
            <td>`[]`</td>
            <td>Yes</td>
        </tr>
        <tr>
            <td>`externalIds`</td>
            <td>`array[string]`</td>
            <td>An array of external provider and unique identifier pairs that the user has linked to their account. External providers are commonly third-party sign on services such as Facebook, Twitter, Google, PSN, Xbox LIVE. The values are stored as a `:` separated pair (e.g. `facebook:92rj23098f203r209823`) with the first part of the pair denoting a unique provider name and the second part being the provider's unique identifier for the user. <p>Supported providers are:</p><ul><li>`facebook`</li><li>`twitter`</li><li>`google`</li></ul></td>
            <td>No</td>
        </tr>
        <tr>
            <td>`verified`</td>
            <td>`boolean`</td>
            <td>Indicates if ther user's identity has been confirmed. Identity confirmation means that their provided e-mail address or phone number is valid.</td>
            <td>`false`</td>
            <td>Yes</td>
        </tr>
    </tbody>
</table>

The JWT token can be provided for each request by one of three methods.

<ul>
    <li>Authorization header</li>
    <li>Cookie<li>
    <li>Query Parameter</li>
</ul>

## Authorization Header

The service will accept an Authorization containing a JWT token where the scheme name is either `JWT` or `Bearer`.

Example:

```txt
Authorization: JWT 9879hf329f8h2fo3ho872hf98f97923fy98uhfioufo32ijf3298fyu9fjh2983hj3289fj32893j2f9jf2f8
```

```txt
Authorization: Bearer 9879hf329f8h2fo3ho872hf98f97923fy98uhfioufo32ijf3298fyu9fjh2983hj3289fj32893j2f9jf2f8
```

## Cookie

The service will also accept the JWT token as sent as a cookie with the name `jwt`.

Example:

```txt
GET / HTTP/1.1
Host: api.example.com
Cookie: jwt=9879hf329f8h2fo3ho872hf98f97923fy98uhfioufo32ijf3298fyu9fjh2983hj3289fj32893j2f9jf2f8
```

## Query Parameter

The service will accept the JWT token as passed in using the `jwt_token` query parameter for any request. As such the `jwt_token` name is also considered a reserved word and should not be used for any schemas or additional request parameters.

Example:

```txt
GET /users/me?jwt_token=9879hf329f8h2fo3ho872hf98f97923fy98uhfioufo32ijf3298fyu9fjh2983hj3289fj32893j2f9jf2f8
Host: api.example.com
```

## Administrative Access

It is expected that the developer (you) will decide the level of access that each role, that a given user is a member of, will have access to by implementing the necessary logic in the various route handlers for any service. However, if you are using the [Account Services](docs/account_services) service to provide authentication services for your platform then it must be noted that there exists a default `admin` role which is intended to have full administrative access to all platform resources. Keep this in mind when developing your code to ensure that this role maintains the level of control that has been intended.

## Requiring Authentication

By default, the service will perform optional authenticate for any JWT access token provided by one of the three methods described above. If a user cannot be authenticated the request is allowed with the `req.user` having a `undefined` value. It is assumed in this circumstance that the request is being made as an Anonymous user.

To require user authentication for any given Path add a Security block for any Path object requiring authentication, specifying "jwt" as the security scheme.

```javascript
"paths": {
    "/items": {
      "get": {
        ...
        "security": [
          {
            "jwt": []
          }
        ]
      },
      ...
```

In code this is accomplished by decorating the route handler function with the `@Auth` decorator as shown below.

```javascript
@Auth()
@Get()
private create(obj: MyObject): Promise<MyObject> {
    ...
}
```

As a matter of convenience you may use the `@RequiresRole` decorator to indicate which roles a user must have for the route to be processed successful. When specified, any user that does not have at least one of the routes specified will be rejected with a `403 FORBIDDEN` response.

```javascript
@Auth()
@Get()
@RequiresRole("admin")
private create(obj: MyObject): Promise<MyObject> {
    ...
}
```

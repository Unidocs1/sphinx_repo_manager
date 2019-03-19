---
title: "1.0.0.alpha"
---

Provides push-based notifications from any AcceleratXR Core service to any client through the use of WebSockets based upon [socket.io](https://socket.io).

## Namespace

Socket.io allows for the capability to multi-plex traffic into different namespaces. This service makes use of this by registering all connections to a pre-configured `namespace` (see [Configuration](#Configuration)).

## Rooms

Rooms provide a means of establishing a channel by which multiple client connections can listen to messages on. When a client successfully makes a socket.io connection they are automatically registered to the following rooms.

| Room Name  | Description                                                                                                    |
| ---------- | -------------------------------------------------------------------------------------------------------------- |
| `allusers` | Default room by which all registered clients can be notified of system wide messages.                          |
| `<userid>` | A user specific room matching the UUID of the user. This room is used to send a specific user direct messages. |

## Registering for Push-Notifications

In order for a client to register for push-notifications an authenticated socket.io request is sent to the `/notifications` path. Clients must authenticate with the service by passing in a proper JWT token (see [cruds_template#Security](https://gitlab.com/AcceleratXR/Core/cruds_template/blob/master/README.md#security) for more information). Unauthenticated clients will be automatically disconnected and will not receive push notifications.

## Sending Push Messages

### From Node.js

In order to send a push message to a client from any NodeJS based application or service the [socket-io.emitter](https://github.com/socketio/socket.io-emitter) library is needed.

You will need to set the appropriately configured `namespace` in order for messages to be received properly by the client.

```javascript
// Connect to socket.io via redis for the namespace axr
var socketio = require("socket.io-emitter")({ host: "localhost", port: 6379 }).of("/axr");

// Send to all clients
socketio.to("allusers").emit("msg" /* ... */);

// Send to individual user
socketio.to(/** user.uid **/).emit("msg" /** ... **/);
```

## Configuration

The service uses the [nconf](https://github.com/indexzero/nconf) configuration system. This configuration system allows simple configuration of variables in an object oriented way that allows each variable to be overridden as command line arguments or by the environment. All configuration defaults for the service are defined and specified in the `config.js` file located at the project root.

### `socket.io`

All configuration settings that apply to the service's use of [socket.io](https://socket.io).

#### `namespace`

In order to isolate messaging traffic for all clients a single global namespace is used for all traffic originating from any AcceleratXR Core based service. The default namespace is `/axr`.

#### `redis`

The redis database is used to allow all other AcceleratXR Core based services to be able to broadcast messages to this service.

The configuration for redis is as follows.

```javascript
{
    // The host name or IP of the redis instance
    'host': 'localhost',
    // The port of the redis instance to connect to
    'port': 6379
}
```

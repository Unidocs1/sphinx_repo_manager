---
title: "1.0.0.alpha"
---

A real-time communication server, based upon [socket.io](https://socket.io/), providing global data synchronization, RPC, and multi-room capability to high performance applications.

## Events

Events are specific types of messages that can be sent between the server and one or more clients. It is possible to define any custom event by simply provided a unique name when sending a message through the socket. However, the following table defines the list of event names that are reserved by the system.

| Event        | Description                                                                                                            |
| ------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `chat`       | Sends a rich-text message to a match or team's chat room.                                                              |
| `kick`       | Disconnects and removes a user from the match/server.                                                                  |
| `kicked`     | Notifies clients that a user has been removed from the server.                                                         |
| `login`      | Sent when a new user logs in to the server.                                                                            |
| `logout`     | Sent when an existing user disconnects, logs out or is kicked from the server.                                         |
| `promote`    | Promotes a user to be host.                                                                                            |
| `promoted`   | Notifies clients that a new host user has been promoted.                                                               |
| `state`      | Used to notify the server and all clients of server state changes.                                                     |
| `state_user` | Used to notify the server and all clients of user state changes.                                                       |
| `rpc`        | Notifies the server and all clients to execute a remote procedure call to some function with an optional data payload. |
| `rpc_server` | Notifies the server to execute a remote procedure call to some function with an optional data payload.                 |
| `rpc_client` | Notifies all clients to execute a remote procedure call to some function with an optional data payload.                |
| `voip`       | Sends a Voice over IP packet to all room members.                                                                      |

### Chat [`chat`]

Users can send rich-text messages to one another using the `chat` event when targeting a specific match or team chat room.

The data payload for an `chat` event MUST be a JSON object containing the following fields.

| Field Name | Type   | Description                                                          |
| ---------- | ------ | -------------------------------------------------------------------- |
| messageUid | string | The universally unique identifier of the message.                    |
| timestamp  | string | The date and time that the message was sent in RFC 3339 format.      |
| senderUid  | uuid   | The universally unique identifier of the user that sent the message. |
| message    | string | The contents of the message.                                         |

#### Example

```javascript
socket.to("/axr/match/<uid>/chat").emit("chat", {
    timestamp: "2009-09-28T19:03:12Z",
    senderUid: "5ac1fb38-24b6-427c-89c8-fdab22b5f2d5",
    message: "Hello world!"
});
```

Server side content filtering is additionally supported as all messages are sent to the special server side function `global.onChat` to be filtered. As a result clients may receive multiple messages with the same `messageUid`. In such a case, the client should locally overwrite the contents of the message with the copy received by the server.

### Login [`login`]

When a new user connects to and joins the server the `login` event is automatically sent to all clients. The event does not have a room designation and is instead considered global.

The message format MUST be a string representing the UUID of the user that has joined.

#### Example

```javascript
socket.on('login', (from, userUid) {
   console.log("User " + userUid + " has joined the server.");
});
```

### Logout [`logout`]

When an existing user loses connection, quits or is kicked from the server the `logout` event is automatically sent to all clients. The event does not have a room designation and is instead considered global.

The message format MUST be a string representing the UUID of the user that has left.

#### Example

```javascript
socket.on('logout', (from, userUid) {
   console.log("User " + userUid + " has left the server.");
});
```

### Kick [`kick`]

To remove a user from the server the `kick` event is used. The `kick` event can only be sent by the match host or the server itself.

The message format MUST be a string representing the UUID of the user to kick.

#### Example

```javascript
socket.to("/axr/match/<uid>").emit("kick", "5ac1fb38-24b6-427c-89c8-fdab22b5f2d5");
```

### Kicked [`kicked`]

When a user has been removed from the server the `kicked` event is broadcast to all clients.

The message format MUST be a string representing the UUID of the user that has been kicked.

#### Example

```javascript
socket.on('kicked', (from, userUid) {
   console.log("User " + userUid + " was kicked from the server.");
});
```

### Promote [`promote`]

The `promote` event can be sent by the match host in order to change hosting responsibility of the server to another user.

The message format MUST be a string representing the UUID of the user to promote.

#### Example

```javascript
socket.to("/axr/match/<uid>").emit("promote", "5ac1fb38-24b6-427c-89c8-fdab22b5f2d5");
```

### Promoted [`promoted`]

When a user has been promoted to server host the `kicked` event is broadcast to all clients.

The message format MUST be a string representing the UUID of the user that has been promoted.

#### Example

```javascript
socket.on('promoted', (from, userUid) {
   console.log("User " + userUid + " is now the host.");
});
```

### State [`state`]

The state event is used to communicate changes in variable data within a given room. Only the server or match `host` is allowed to send messages for the `state` event.

The message format MUST be a JSON object with each key-value pair mapping to the name of a variable and its value.

#### Example

```javascript
socket.to('/axr/match/<uid>').emit('state',
    {
        myString: 'value',
        myBool: true,
        myInt: 3,
        ...
    }
);
```

When it is desired to represent binary data in the global state a [ArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer) or [Buffer](https://nodejs.org/api/buffer.html) should be used wrapped in the JSON object as a member.

#### Example (binary)

```javascript
socket.to('/axr/match/<uid>').emit('state',
    {
        buffer: Buffer.from([1,2,3,...]);
    }
);
```

### State [`state_user`]

This event is used to communicate changes about a particular user to a room. Only the user for which the state change belongs to may send events of this type.

The message format MUST be an arbitrary JSON object with each key-value pair mapping to the name of a variable and its value. The object MUST also contain a `userUid` field containing the unique identifier of the user the state object represents.

#### Example

```javascript
socket.to('/axr/match/<uid>').emit('state_user',
    {
        userUid: '5ac1fb38-24b6-427c-89c8-fdab22b5f2d5',
        myString: 'value',
        myBool: true,
        myInt: 3,
        ...
    }
);
```

### Remote Procedure Calls [`rpc`, `rpc_client`, `rpc_server`]

An remote procedure call (RPC) can be sent between clients and the server using an `rpc` event. There are three types of RPC events.

| Event        | Description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| `rpc`        | Executes a remote procedure call on server and all clients simultaneously. |
| `rpc_client` | Executes a remote procedure call on clients only.                          |
| `rpc_server` | Executes a remote procedure call on the server only.                       |

The data payload for an RPC event MUST be a JSON object containing the following fields.

| Field Name | Type       | Description                                      |
| ---------- | ---------- | ------------------------------------------------ |
| name       | string     | The name of the function to execute.             |
| args       | array[any] | An array of arguments to pass into the function. |

#### Example (client)

```javascript
socket.emit('rpc',
    {
        name: 'fireWeapon',
        args: ["playerUid", {x: 0, y: 0, z: 0}]
    }
);

/**
 * Called when a player has fired their weapon at a target.
 *
 * @param {string} The unique identifier of the player firing the weapon.
 * @param {vector3} The vector referencing the target that the player has fired against.
 */
const fireWeapon = function (playerUid, target) {
    if (/** isValid **/) {
        /** apply damage to target **/
    }
};
```

In the above example the client calls the global `fireWeapon` function on all clients and the server. It should be noted that the `rpc` event does not specify a room and is instead emitted directly to the socket connection.

#### Example (server)

```javascript
/**
 * Called when a player has fired their weapon at a target.
 *
 * @param {string} The unique identifier of the player firing the weapon.
 * @param {vector3} The vector referencing the target that the player has fired against.
 */
const fireWeapon = function (playerUid, target) {
    if (/** isValid **/) {
        /** apply damage to target **/
    }
};
```

In the above examples all RPC functions do not return a result. This is because events in socket.io are not a request that can return a response. However, as a matter of convenience the server can automatically send a response event back to the client containing the result. The name of the response event is the same as the original event with `Result` appended to the end. Therefore, if an RPC function named `addHP` is defined that returns the current amount of player health then the server will automatically send an `rpc` event to the client named `addHPResult` containing the result as its single argument.

#### Example (returning a result)

```javascript
// client.js
socket.emit("rpc", {
    name: "addHP",
    args: [50]
});

const addHPResult = function(health) {
    console.log("Player has " + health + " health");
};

// server.js
const addHP = function(amount) {
    return userHP + amount;
};
```

### Voice Over IP [`voip`]

The use of Voice over IP is also supported by the server and can be sent to any room's `chat` channel using the `voip` event. This makes it possible to easily filter out VOIP traffic by match or by team.

The data payload for a `voip` event MUST be a JSON object containing the following fields.

| Field Name | Type   | Description                                                          |
| ---------- | ------ | -------------------------------------------------------------------- |
| timestamp  | string | The date and time that the message was sent in RFC 3339 format.      |
| senderUid  | uuid   | The universally unique identifier of the user that sent the message. |
| data       | Buffer | A binary buffer containing the raw voice data.                       |

#### Example (Match)

```javascript
socket.to("/axr/match/<uid>/chat").emit("voip", {
    timestamp: "2009-09-28T19:03:12Z",
    senderUid: "5ac1fb38-24b6-427c-89c8-fdab22b5f2d5",
    data: Buffer.from(/** voip packet **/)
});
```

#### Example (Team)

```javascript
socket.to("/axr/match/<uid>/teams/<teamId>/chat").emit("voip", {
    timestamp: "2009-09-28T19:03:12Z",
    senderUid: "5ac1fb38-24b6-427c-89c8-fdab22b5f2d5",
    data: Buffer.from(/** voip packet **/)
});
```

## Matches

The RTC server optionally works with [matchmaking_services](https://gitlab.com/AcceleratXR/Core/matchmaking_services) to provide a simple solution for real-time networking of multi-player games and experiences. When a match id is specified (using the `matchUid` cli option) information is retrieved from the pre-configured match service (see [Configuration](#Configuration)) to determine what users are allowed to join the server as well as the teams that are available and their configuration.

### Rooms

Upon a client connection, users are automatically added to the following based rooms.

-   `/<matchUid>` - Used for all match/server wide communication. Typically used to synchronize global state and process RPC commands.
-   `/<matchUid>/chat` - Provides global rich-text chat capability to all clients.
-   `/<matchUid>/teams/<teamId>` - Used for all team wide communication. Allows synchronization of team-specific data.
-   `/<matchUid>/teams/<teamId>/chat` - Provides rich-text chat capability to all team members.

## Custom Logic

Custom logic can be added to the server to handle any RPC command sent by a client. All custom code is placed into the `custom` folder by adding any number of `.js` files. All `.js` files contained in the `custom` folder (including files in sub-directories) is loaded at server start up.

To request a execute a function contained in one of the custom files the path of the module file is used (relative to the `custom` folder) followed by a `.` and the name of the function.

For example, if you've created a module called `myModule.js` and defined a function named `myFunc` in that module you would reference the RPC function as `myModule.myFunc`.

Modules contained in sub-directories are also supported by simply pre-pending the path to the module. Therefore if you've created a module such as `utils/MyUtilsModule.js` and want to call it's `myUtilFunc` function the correct RPC name is `utils/MyUtilsModule.myUtilFunc`.

### Global Functions

A special `global.js` file is provided by default. It is special because any function defined and exported in this file can be addressable simply by name.

For example if you define a function named `myGlobalFunc` in the `global.js` and wish to call this function from a client the name can simply be `myGlobalFunc`. However, specifying `global.myGlobalFunc` will also work.

#### Default Functions

By default, a set of default functions are defined in the `global.js` file which correspond to common events originating from the server. The following table describes these default functions.

| Function Name       | Declaration                                      | Description                                                                |
| ------------------- | ------------------------------------------------ | -------------------------------------------------------------------------- |
| `onChat`            | `function (room, senderUid, timestamp, message)` | Called when a new chat message is received.                                |
| `onLogin`           | `function (userUid)`                             | Called when a user with the specified id joins the server.                 |
| `onLogout`          | `function (userUid)`                             | Called when a user with the specified id leaves the server.                |
| `onPromoted`        | `function (userUid)`                             | Called when a user with the specified id is promoted to the server host.   |
| `onKicked`          | `function (userUid)`                             | Called when a user with the specified id is removed from the server.       |
| `onStateChanged`    | `function (newState)`                            | Called when the global server state has been modified.                     |
| `onUserStateChange` | `function (userUid, newState)`                   | Called when the state of the user with the specified id has been modified. |

## Configuration

The service uses the [nconf](https://github.com/indexzero/nconf) configuration system. This configuration system allows simple configuration of variables in an object oriented way that allows each variable to be overridden as command line arguments or by the environment. All configuration defaults for the service are defined and specified in the `config.js` file located at the project root.

### `jwt::authToken`

The JSON Web Token (JWT) authorization token to use when performing external service calls (e.g. matchmaking_services).

### `matchService`

Contains configuration information about an external [matchmaking_services](https://gitlab.com/AcceleratXR/Core/matchmaking_services) service that is used to query information about matches when a `matchUid` is provided to the server.

### `socket.io`

All configuration settings that apply to the service's use of [socket.io](https://socket.io). These settings should match those set by all other AcceleratXR Core based services in use.

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

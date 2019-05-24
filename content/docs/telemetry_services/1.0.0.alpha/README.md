
* * *

title: "Telemetry Services"

date: 2019-05-16T22:27:58.817Z
------------------------------

Provides a service for the storage, forwarding and post processing of telemetry events.

Getting Started
---------------

To get started using this service first clone the source. It is highly recommended that you fork the project first.

```bash
git clone {{repository}}
```

Running the Service
-------------------

Open up a new shell to the cloned folder and build the Docker image using `docker-compose`.

```bash
docker-compose build
```

You can now run the server with the following command.

```bash
docker-compose up
```

Debugging
---------

[Visual Studio Code](https://code.visualstudio.com/) is the recommended IDE to develop with. The project includes workspace and launch configuration files out of the box.

To debug while running via Docker Compose select the `Docker: Attach Debugger` configuration and hit the `F5` key. If you want to run the server directly and debug choose the `Launch Server` configuration.

## Index

### Classes

* [AuthToken](classes/authtoken.md)
* [Count](classes/count.md)
* [Event](classes/event.md)
* [EventRoute](classes/eventroute.md)
* [MetricsCollector](classes/metricscollector.md)

### Variables

* [bgManager](#bgmanager)
* [cliDefinitions](#clidefinitions)
* [cliOptions](#clioptions)
* [conf](#conf)
* [logger](#logger)
* [packageInfo](#packageinfo)
* [server](#server)

### Functions

* [start](#start)

---

## Variables

<a id="bgmanager"></a>

### `<Let>` bgManager

**● bgManager**: *`BackgroundServiceManager`* =  undefined

*Defined in server.ts:20*

___
<a id="clidefinitions"></a>

### `<Const>` cliDefinitions

**● cliDefinitions**: *`OptionDefinition`[]* =  []

*Defined in server.ts:17*

___
<a id="clioptions"></a>

### `<Const>` cliOptions

**● cliOptions**: *`CommandLineOptions`* =  commandLineArgs(cliDefinitions)

*Defined in server.ts:18*

___
<a id="conf"></a>

### `<Const>` conf

**● conf**: *`any`* =  require("nconf")
    .argv()
    .env({
        separator: "__",
        parseValues: true,
    })

*Defined in config.ts:5*

___
<a id="logger"></a>

### `<Const>` logger

**● logger**: *`any`* =  Logger()

*Defined in server.ts:14*

___
<a id="packageinfo"></a>

### `<Const>` packageInfo

**● packageInfo**: *`any`* =  require("../package.json")

*Defined in config.ts:4*

___
<a id="server"></a>

### `<Let>` server

**● server**: *`Server`* =  undefined

*Defined in server.ts:19*

___

## Functions

<a id="start"></a>

### `<Const>` start

▸ **start**(config: *`any`*, logger: *`any`*): `Promise`<`void`>

*Defined in server.ts:22*

**Parameters:**

| Name | Type |
| ------ | ------ |
| config | `any` |
| logger | `any` |

**Returns:** `Promise`<`void`>

___


---
title: "Reference"
date: 2019-05-22T10:58:00-08:00
---

### Classes

-   [AuthToken](classes/authtoken)
-   [Count](classes/count)
-   [MetricsCollector](classes/metricscollector)
-   [Persona](classes/persona)
-   [PersonaRoute](classes/personaroute)
-   [PersonaStat](classes/personastat)
-   [PersonaStatDefinition](classes/personastatdefinition)
-   [PersonaStatDefinitionRoute](classes/personastatdefinitionroute)
-   [PersonaStatRoute](classes/personastatroute)

### Variables

-   [bgManager](#bgmanager)
-   [cliDefinitions](#clidefinitions)
-   [cliOptions](#clioptions)
-   [conf](#conf)
-   [logger](#logger)
-   [packageInfo](#packageinfo)
-   [server](#server)

### Functions

-   [start](#start)

---

## Variables

<a id="bgmanager"></a>

### `<Let>` bgManager

**● bgManager**: _`BackgroundServiceManager`_ = undefined

_Defined in server.ts:20_

---

<a id="clidefinitions"></a>

### `<Const>` cliDefinitions

**● cliDefinitions**: _`OptionDefinition`[]_ = []

_Defined in server.ts:17_

---

<a id="clioptions"></a>

### `<Const>` cliOptions

**● cliOptions**: _`CommandLineOptions`_ = commandLineArgs(cliDefinitions)

_Defined in server.ts:18_

---

<a id="conf"></a>

### `<Const>` conf

**● conf**: _`any`_ = require("nconf")
.argv()
.env({
separator: "\_\_",
parseValues: true,
})

_Defined in config.ts:5_

---

<a id="logger"></a>

### `<Const>` logger

**● logger**: _`any`_ = Logger()

_Defined in server.ts:14_

---

<a id="packageinfo"></a>

### `<Const>` packageInfo

**● packageInfo**: _`any`_ = require("../package.json")

_Defined in config.ts:4_

---

<a id="server"></a>

### `<Let>` server

**● server**: _`Server`_ = undefined

_Defined in server.ts:19_

---

## Functions

<a id="start"></a>

### `<Const>` start

▸ **start**(config: _`any`_, logger: _`any`_): `Promise`<`void`>

_Defined in server.ts:22_

**Parameters:**

| Name   | Type  |
| ------ | ----- |
| config | `any` |
| logger | `any` |

**Returns:** `Promise`<`void`>

---

[telemetry_services](../README.md) > [MetricsCollector](../classes/metricscollector.md)

# Class: MetricsCollector

The `MetricsCollector` provides a background service for collecting Prometheseus metrics for consumption by external clients and compatible servers using the built-in `MetricsRoute` route handler.

*__author__*: Jean-Philippe Steinmetz [info@acceleratxr.com](mailto:info@acceleratxr.com)

## Hierarchy

 `BackgroundService`

**↳ MetricsCollector**

## Index

### Constructors

* [constructor](metricscollector.md#constructor)

### Properties

* [config](metricscollector.md#config)
* [logger](metricscollector.md#logger)
* [registry](metricscollector.md#registry)

### Methods

* [run](metricscollector.md#run)
* [start](metricscollector.md#start)
* [stop](metricscollector.md#stop)

---

## Constructors

<a id="constructor"></a>

###  constructor

⊕ **new MetricsCollector**(config: *`any`*, logger: *`any`*): [MetricsCollector](metricscollector.md)

*Overrides BackgroundService.__constructor*

*Defined in jobs/MetricsCollector.ts:14*

**Parameters:**

| Name | Type |
| ------ | ------ |
| config | `any` |
| logger | `any` |

**Returns:** [MetricsCollector](metricscollector.md)

___

## Properties

<a id="config"></a>

### `<Protected>` config

**● config**: *`any`*

*Inherited from BackgroundService.config*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/utilities/dist/types/BackgroundService.d.ts:9*

The global application configuration that the service can reference.

___
<a id="logger"></a>

### `<Protected>` logger

**● logger**: *`any`*

*Inherited from BackgroundService.logger*

*Defined in C:/Users/jpsaxr/gitlab/telemetry_services/node_modules/@acceleratxr/utilities/dist/types/BackgroundService.d.ts:11*

The logging utility to use.

___
<a id="registry"></a>

### `<Private>` registry

**● registry**: *`Registry`*

*Defined in jobs/MetricsCollector.ts:14*

___

## Methods

<a id="run"></a>

###  run

▸ **run**(): `void`

*Overrides BackgroundService.run*

*Defined in jobs/MetricsCollector.ts:21*

**Returns:** `void`

___
<a id="start"></a>

###  start

▸ **start**(): `Promise`<`void`>

*Overrides BackgroundService.start*

*Defined in jobs/MetricsCollector.ts:25*

**Returns:** `Promise`<`void`>

___
<a id="stop"></a>

###  stop

▸ **stop**(): `Promise`<`void`>

*Overrides BackgroundService.stop*

*Defined in jobs/MetricsCollector.ts:27*

**Returns:** `Promise`<`void`>

___


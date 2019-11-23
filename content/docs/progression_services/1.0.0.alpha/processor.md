---
title: "Event Processor"
date: 2019-11-22T23:48:48.249Z
---

The `EventProcessor` is a background service whose responsibility it is to process events that have been scraped and placed on the redis queue `ps.events`.

The processor requires that each event meets the following criteria.

The event data must:

1. Contain a `type` field mapping to a skill requirement.
2. Contain a `personaUid` or `userUid` field mapping to a given player being tracked.
3. Contain a `value` field containing the amount of change being tracked.

If any of the above information is missing the event is rejected.

When processing a given event all **enabled** skills for the given `personaUid` are retrieved that have at least one requirement for the given event `type`. This simplifies the unlock and availability discovery required by the client application.

Since the `value` type can be any supported JSON type there a couple of rules to consider. The processor will treat different types differently in order to make the best decision about how the requirement is met.

## `Number` Values

When a `number` value is used it is incrementally added to the progress value. Therefore, if the current progress value is `5` and the event contains value `3` the new value of the progress will be `8`.

## `String` / `Boolean` Values

String and boolean values are compared for strict equality using the `===` operator. This means that the values must exactly match in order to be considered complete. When updating the progress with these types the previous value is replaced with the event's new value.

## Object Values

Object values can also be used but are generally discouraged as they require more processing time and resources. Like strings and boolean they are compared with a strict equality of the serialized value of the object. Similarly, the value of the progress is replaced instead of incremented since no assumptions can be made about the object structure.

It is important to note that objects, when compared for completion, are serialized to string JSON form first before being compared against the required value. This eliminates issues with comparing objects in memory directly but has the downside of using more processing power and resources to perform the comparison. As such it is recommended to use objects sparingly.

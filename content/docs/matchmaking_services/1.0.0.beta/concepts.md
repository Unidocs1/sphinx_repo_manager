---
title: "Concepts"
date: 2019-05-22T10:50:00-08:00
---

The following key concepts and terminology will be used throughout the rest of this documentation.

## Tickets

A matchmaking ticket is a representation of a single user or group that wants to be matched with other like users or groups. It contains all information needed for a Ticket Processor to perform its work.

### Criteria

The most important information a ticket contains is about the type of search to perform. This is called the search criteria. Search criteria is intended to be arbitrary and definable by the implementing product. In order to make the definition of criteria easier, values are limited to simple data types such as integers, booleans, strings and doubles. Complex objects are not allowed. Each criteria allows the specification of min and max values to search for. Thus it is possible to specify a range of desired values for any single criteria. Ranges are inclusive by default. Therefore if it is desired to search for all `skill` values from `[1250, 1750]` you must specify `minValue` to `1250` and `maxValue` to `1750`. If you wish to express the range `[1250, inf]` specify values simply omit a value for `maxValue`.

### Statistics

Each ticket also includes a set of user and group statistics. Statistics are information about the user or group corresponding to the matchmaking search. It is important that for each set of search criteria a matching statistics value exists. For example, if the ticket includes search criteria for filtering all `skill` values from \[1250-1750\], then the statistics data must include a variable `skill` with the value of the user or group's current skill level (e.g. `1500`). Any ticket that contains search criteria without a matching statistics value is considered invalid and will be rejected.

### Groups

Groups of users can be represented by listing all users in the ticket. A single user in a group must be designated as the ticket holder. That user is responsible for submitting the ticket and maintaining its state. Other users may query the ticket but only the ticket holder may update information on the ticket such as search criteria or statistics.

## Session

Once a suitable collection of users are identified that can be grouped together a `Session` object is created. The `Session` object contains information about the members of the match as well as metadata information about the match criteria.

## Processors

A Ticket Processor is a specialized program that is responsible for performing the actual search and matching functionality of the matchmaking process. The processor will retrieve a subset of tickets from the database at a given time, sorting and filtering all tickets whose search criteria are comparable. If a suitable subset is found, then all tickets in the subset are updated to inform users that the match has been found.

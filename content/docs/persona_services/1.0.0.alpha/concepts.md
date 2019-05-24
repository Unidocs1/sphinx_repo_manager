---
title: "Concepts"
date: 2019-05-22T10:58:00-08:00
---

## Persona

The `Persona` is a particular representation of a user in the virtual world. This is also often referred to as a user avatar or player character. Each Persona has a `name` that uniquely identifies them from others within the world. They also feature a set of attributes and statistics. The attributes and statistics are entirely arbitrary and defined by the developer as described later in this chapter.

### Attributes

Attributes allow you to describe any characteristic that a given `Persona` can have. These characteristics can be discrete values or higher level concepts that link to other structures. For an example, assume we are building an fantasy MMORPG. A typical set of attributes for each character in this game may include the following.

-   `age` - The descriptive age of the Persona as defined by the user
-   `bio` - The descriptive history of the Persona as defined by the user
-   `class` - The character archetype expressed as an enumerated value. e.g. `Warrior`, `Wizard`, `Necromancer`, `Priest`
-   `race` - The humanoid race that the Persona belongs to. e.g. `Dwarf`, `Elf`, `Human`, `Time Lord`

These can be easily represented in the `attributes` property of a `Persona` object.

```javascript
{
    "userUid": "d4c61b75-9141-4383-af25-b2a254b95b21",
    "name": "Jon Snow",
    "description": "Jon Snow is a character from the book A Song of Fire and Ice by George R.R. Martin.",
    "attributes": {
        "age": 26,
        "alias": "Aegon Targaryen",
        "bio": "Commander of the Night's Watch. King of the North. Protector of the living.",
        "class": "warrior",
        "race": "human"
    }
}
```

## PersonaStat

Similar to attributes the `PersonaStat` is a type of statistic associated with a given `Persona` that describes the abilities of that particular character. In contrast to attributes the `PersonaStat` has a well defined structure to make it easier to perform calculations and comparisons of like statistics from other `Persona` objects.

The `PersonaStat` object defines a given statistic that has been associated with a particular `Persona` and the value that has been assigned to it.

A typical `PersonaStat` object looks like the following.

```javascript
{
    "personaUid": "bdf1b0e0-7e61-4069-b37b-bb73919b561b",
    "statUid": "f0d2ef5e-40a3-4d70-9d37-2e284aaf4986",
    "value": <value>
}
```

## PersonaStatDefinition

The `PersonaStatDefinition` is a definition of a given statistic that can be associated with any given `Persona` object. It has a set of properties that clearly define the boundaries of a statistic in order to simply code when performing comparison and computation against other statistics of like values.

Each statistic must define one or all of the following properties.

-   `type` - The data type of the statistic's value. Must be a valid JavaScript data type. Possible values are `boolean`, `number`, `bigint`, `string` and `object`.
-   `min` - The minimum value that is possible to assign to an associated `Persona`. Useful in describing a range of values.
-   `max` - The maximum value that is possible to assign to an associated `Persona`. Useful in describing a range of values.
-   `values` - A list of pre-defined values that the statistic can have. Useful when describing an enumerator.
-   `default` - The initial value that will be given to all `Persona` objects that have a stat associated with them.

When defining a definition the types of `min`, `max`, `values` and `default` must all be the same and must be of the same type as described by the `type` property. If the types are different the definition will be rejected upon creation. In the case of the `object` type no validation is performed other than to verify than a given value is a valid JavaScript object (e.g. `{}`).

Using this definition it is possible to define many different types of statistic values.

### Example Number

The following example illustrates how to define a statistic with numerical values that range from `0` to `100` with a default value of `0`.

```javascript
{
    "name": "MyNumericalStat",
    "type": "number",
    "min": 0,
    "max": 100,
    "default": 0
}
```

### Example String Enumerator

The following example illustrates how to define an enumerated value of strings.

```javascript
{
    "name": "MyEnumeratedStringStat",
    "type": "string",
    "values": [
        "A",
        "B",
        "C",
        "D"
    ],
    "default": "A"
}
```

### Example Number Enumerator

The following example illustrates how to define an enumerated value of numbers.

```javascript
{
    "name": "MyEnumeratedNumberStat",
    "type": "number",
    "values": [
        0,
        1,
        2,
        3,
    ],
    "default": 0
}
```

### Example Object

The following example illustrates how to define an statistic with an object value.

```javascript
{
    "name": "MyObjectStat",
    "type": "object",
    "values": [
        { prop: 0 },
        { prop: 1 },
        { prop: 2 },
        { prop: 3 },
    ],
    "default": { prop: 0 }
}
```

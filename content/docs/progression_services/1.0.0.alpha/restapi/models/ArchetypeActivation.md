---
title: "ArchetypeActivation"
date: 2019-11-22T23:48:48.249Z
---

Describes whether or not a archetype should be enabled for the given persona.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [enabled](#enabled) | Set to `true` to enable the archetype for the given persona. Otherwise set to `false` to disable the archetype. | `boolean` |  | `true` | false | false | true |

## Examples
### Request

```json
{
    "enabled": false
}
```

### Response

```json
{
    "enabled": false
}
```


## Members

### enabled

Type: `boolean`

Default Value: `true`

Required: `true`

Set to `true` to enable the archetype for the given persona. Otherwise set to `false` to disable the archetype.

## References

This data model is referenced in the following endpoints.

// TODO
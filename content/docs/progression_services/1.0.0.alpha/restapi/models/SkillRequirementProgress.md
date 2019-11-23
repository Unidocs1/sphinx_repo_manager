---
title: "SkillRequirementProgress"
date: 2019-11-22T23:48:48.249Z
---

Tracks the persona's progress of a single requirement for a given skill.

The following is the list of all members included in the data model.

| Member            | Description                         | Type | Format / Schema | Default Value | Identifier | Unique | Required |
| ----------------- | ----------------------------------- | ---- | ------ | ------------- | ---------- | ------ | -------- |
| [requirementUid](#requirementUid) | The unique identifier of the requirement being tracked. | `string` |  | `""` | false | false | true |
| [value](#value) | The current value of the player's progress. | `object` |  | `undefined` | false | false | true |

## Examples
### Request

```json
{}
```

### Response

```json
{
    "requirementUid": "string"
}
```


## Members

### requirementUid

Type: `string`

Default Value: `""`

Required: `true`

The unique identifier of the requirement being tracked.

### value

Type: `object`

Default Value: `undefined`

Required: `true`

The current value of the player's progress.

## References

This data model is referenced in the following endpoints.

// TODO
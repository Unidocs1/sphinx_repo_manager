---
title: "Tutorial: RPG Classes"
date: 2019-11-22T23:48:48.249Z
---

This guide will show you how to create a multi-dimensional skill tree with branching. The concepts described build upon the previous [Tutorial: Level System](tutorial_levels) and will reference the level system described in the examples.

To illustrate this we will create a simple class system typical of any role playing game (RPG). The system will consist of three classes: `Bard`, `Mage` and `Paladin`. Each class is defined as a single archetype with a unique set of skills. The skills in each class will have a complex hierarchy in order to show how it is possible to create multi-dimensional skill trees.

## Pre-requisites

This guide assumes you have read and understand the following documents:

-   [Tutorial: Level System](tutorial_levels)

## Mage Class

The `Mage` is a magical sorceror that has a myraid of abilities powered by the four physical elements.

The following table illustrates the set of skills that will be awarded at particular levels and their other skill requirements.

| Skill              | Description                                                                              | Requires              |
| ------------------ | ---------------------------------------------------------------------------------------- | --------------------- |
| ice_blast          | Hurl an icy blast at your enemy and deal 10 damage.                                      | N/A                   |
| fire_grenade       | Send a grenade of hot fire towards your enemy and deal 20 damage across a 5 foot radius. | N/A                   |
| snare              | Snare your enemy with tree roots for 15 seconds.                                         | N/A                   |
| ice_blast_advanced | Hurl an icy blast at your enemy and deal 20 damage.                                      | level_3, ice_blast    |
| fire_bomb          | Send a bomb of hot fire towards your enemy and deal 40 damage across a 10 foot radius.   | level_5, fire_grenade |
| snare_thick        | Snare your enemy with thick tree roots for 30 seconds.                                   | level_7, snare        |
| fire_storm         | Send a storm of hot fire towards your enemy and deal 60 damage across a 25 foot radius.  | level_10, fire_bomb   |

This tree can be encoded into JSON to be created with the service as follows.

```javascript
[
    {
        uid: "66def31c-c10f-4c22-9ca3-3dd309ca4b98",
        name: "ice_blast",
        title: "Ice Blast",
        description: "Hurl an icy blast at your enemy and deal 10 damage.",
        icon: "ice_blast.png",
        requirements: [],
        data: {
            damage: 10,
            cooldown: 1,
        },
    },
    {
        uid: "fda52e9a-6447-4a61-90c8-9704930d0e8d",
        name: "fire_grenade",
        title: "Fire Grenade",
        description: "Send a grenade of hot fire towards your enemy and deal 20 damage across a 5 foot radius.",
        icon: "fire_grenade.png",
        requirements: [],
        data: {
            damage: 20,
            cooldown: 60,
            radius: 5,
        },
    },
    {
        uid: "f9cc39da-d45e-457d-a4c9-e9eb6ecb65f7",
        name: "snare",
        title: "Root Snare",
        description: "Snare your enemy with tree roots for 15 seconds.",
        icon: "root_snare.png",
        requirements: [],
        data: {
            cooldown: 60,
            snare: 15,
        },
    },
    {
        uid: "9ca00f56-d813-4335-aa5f-a756ef64d30c",
        name: "ice_blast_advanced",
        title: "Advanced Ice Blast",
        description: "Hurl an icy blast at your enemy and deal 20 damage.",
        icon: "ice_blast_advanced.png",
        requirements: [
            {
                type: "SkillUnlocked",
                title: "Ice Blast",
                description: "Requires Ice Blast.",
                icon: "ice_blast.png",
                value: "66def31c-c10f-4c22-9ca3-3dd309ca4b98",
            },
            {
                type: "SkillUnlocked",
                title: "Level 3",
                description: "Requires Level 3.",
                icon: "level3.png",
                value: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
            },
        ],
        data: {
            damage: 20,
            cooldown: 1,
        },
    },
    {
        uid: "fec0699d-9e83-489f-a2d1-4916b577d74f",
        name: "fire_bomb",
        title: "Fire Bomb",
        description: "Send a bomb of hot fire towards your enemy and deal 40 damage across a 10 foot radius.",
        icon: "fire_bomb.png",
        requirements: [
            {
                type: "SkillUnlocked",
                title: "Fire Grenade",
                description: "Requires Fire Grenade.",
                icon: "fire_grenade.png",
                value: "fda52e9a-6447-4a61-90c8-9704930d0e8d",
            },
            {
                type: "SkillUnlocked",
                title: "Level 5",
                description: "Requires Level 5.",
                icon: "level5.png",
                value: "e53768f4-df1e-497d-8e75-87beebc0cd23",
            },
        ],
        data: {
            damage: 40,
            cooldown: 60,
            radius: 10,
        },
    },
    {
        uid: "531db201-0d36-47e6-8356-3607e3b199a2",
        name: "snare_thick",
        title: "Thick Root Snare",
        description: "Snare your enemy with thick tree roots for 30 seconds.",
        icon: "snare_thick.png",
        requirements: [
            {
                type: "SkillUnlocked",
                title: "Root Snare",
                description: "Requires Root Snare.",
                icon: "root_snare.png",
                value: "f9cc39da-d45e-457d-a4c9-e9eb6ecb65f7",
            },
            {
                type: "SkillUnlocked",
                title: "Level 7",
                description: "Requires Level 7.",
                icon: "level7.png",
                value: "fde448ce-5fb2-423b-a3b0-f84d9ce8a1b9",
            },
        ],
        data: {
            cooldown: 60,
            snare: 30,
        },
    },
    {
        uid: "2f8a85a8-4254-4f1a-a65e-e991e1a69c69",
        name: "fire_storm",
        title: "Fire Storm",
        description: "Send a storm of hot fire towards your enemy and deal 60 damage across a 25 foot radius.",
        icon: "fire_storm.png",
        requirements: [
            {
                type: "SkillUnlocked",
                title: "Fire Bomb",
                description: "Requires Fire Bomb.",
                icon: "fire_bomb.png",
                value: "fec0699d-9e83-489f-a2d1-4916b577d74f",
            },
            {
                type: "SkillUnlocked",
                title: "Level 10",
                description: "Requires Level 10.",
                icon: "level10.png",
                value: "d0e030c7-c6c1-489f-9096-2c17285b4961",
            },
        ],
        data: {
            damage: 65,
            cooldown: 60,
            radius: 25,
        },
    },
];
```

The archetype definition will reference the three root skills of `ice_blast`, `fire_grenade` and `snare`. The system will then discover the remaning skills in the archetype automatically.

```javascript
{
    name: "mage",
    title: "Mage",
    description: "The Mage is a powerful sorceror that controls the four elements.",
    icon: "mage.png",
    skills: [
        "66def31c-c10f-4c22-9ca3-3dd309ca4b98",
        "fda52e9a-6447-4a61-90c8-9704930d0e8d",
        "f9cc39da-d45e-457d-a4c9-e9eb6ecb65f7",
    ],
    data: undefined,
}
```

## Paladin Class

The `Paladin` is a holy warrior blessed by the Gods with supernatural strength.

The following table illustrates the set of skills that will be awarded at particular levels and their other skill requirements.

| Skill         | Description                                                               | Requires                     |
| ------------- | ------------------------------------------------------------------------- | ---------------------------- |
| shield        | Protects the user from 10 damage for 5 seconds.                           | N/A                          |
| slash         | Slash enemy with your broad sword for 10 damage.                          | N/A                          |
| heal          | Heal yourself for 10 hit points.                                          | N/A                          |
| heavy_shield  | Protects the user from 20 damage for 10 seconds.                          | level_3, shield              |
| hack_n_slash  | Hack and slash your enemy for 15 damage.                                  | level_5, slash               |
| heal_advanced | Heal yourself for 20 hit points.                                          | level_7, heal                |
| gods_might    | Deal 20 damage to your opponent while healing yourself for 10 hit points. | level_10, heal, heavy_shield |

This tree can be encoded into JSON to be created with the service as follows.

```javascript
[
    {
        uid: "d3f56fd6-9d00-4401-99de-029d5f92d594",
        name: "shield",
        title: "Shield",
        description: "Protects the user from 10 damage for 5 seconds.",
        icon: "shield.png",
        requirements: [],
        data: {
            shield: 10,
            cooldown: 1,
            duration: 5,
        },
    },
    {
        uid: "c4348f24-5c9e-4d84-a404-fa19aee752bb",
        name: "slash",
        title: "Slash",
        description: "Slash enemy with your broad sword for 10 damage.",
        icon: "slash.png",
        requirements: [],
        data: {
            damage: 10,
            cooldown: 1,
        },
    },
    {
        uid: "0e7bb2e2-b6bb-47b0-b51e-392279334254",
        name: "heal",
        title: "Heal",
        description: "Heal yourself for 10 hit points.",
        icon: "heal.png",
        requirements: [],
        data: {
            restore: 10,
            cooldown: 5,
        },
    },
    {
        uid: "65ea5c76-dd3f-43fd-8a27-f89f9bbfa2f5",
        name: "heavy_shield",
        title: "Heavy Shield",
        description: "Protects the user from 20 damage for 10 seconds.",
        icon: "heavy_shield.png",
        requirements: [
            {
                uid: uuid.v4(),
                type: "SkillUnlocked",
                title: "Shield",
                description: "Requires Shield.",
                icon: "shield.png",
                value: "d3f56fd6-9d00-4401-99de-029d5f92d594",
            },
            {
                type: "SkillUnlocked",
                title: "Level 3",
                description: "Requires Level 3.",
                icon: "level3.png",
                value: "1ea968f3-ca97-4d8c-8c9d-63d183942be0",
            },
        ],
        data: {
            shield: 20,
            cooldown: 1,
            duration: 10,
        },
    },
    {
        uid: "7cfc22ef-418d-48e1-8e9a-147e65759f66",
        name: "hack_n_slash",
        title: "Hack 'n Slash",
        description: "Hack and slash your enemy for 15 damage.",
        icon: "hack_n_slash.png",
        requirements: [
            {
                uid: uuid.v4(),
                type: "SkillUnlocked",
                title: "slash",
                description: "Requires Slash.",
                icon: "slash.png",
                value: "c4348f24-5c9e-4d84-a404-fa19aee752bb",
            },
            {
                type: "SkillUnlocked",
                title: "Level 5",
                description: "Requires Level 5.",
                icon: "level5.png",
                value: "e53768f4-df1e-497d-8e75-87beebc0cd23",
            },
        ],
        data: {
            damage: 15,
            cooldown: 1,
        },
    },
    {
        uid: "6c8bf035-58db-4a6b-a34e-c3045cd13c8c",
        name: "heal_advanced",
        title: "Advanced Heal",
        description: "Heal yourself for 20 hit points.",
        icon: "heal_advanced.png",
        requirements: [
            {
                uid: uuid.v4(),
                type: "SkillUnlocked",
                title: "Heal",
                description: "Requires Heal.",
                icon: "heal.png",
                value: "0e7bb2e2-b6bb-47b0-b51e-392279334254",
            },
            {
                type: "SkillUnlocked",
                title: "Level 7",
                description: "Requires Level 7.",
                icon: "level7.png",
                value: "fde448ce-5fb2-423b-a3b0-f84d9ce8a1b9",
            },
        ],
        data: {
            restore: 20,
            cooldown: 1,
            duration: 10,
        },
    },
    {
        uid: "6c8bf035-58db-4a6b-a34e-c3045cd13c8c",
        name: "gods_might",
        title: "God's Might",
        description: "Deal 15 damage to your opponent while healing yourself for 10 hit points.",
        icon: "gods_might.png",
        requirements: [
            {
                uid: uuid.v4(),
                type: "SkillUnlocked",
                title: "Heal",
                description: "Requires Heal.",
                icon: "heal.png",
                value: "0e7bb2e2-b6bb-47b0-b51e-392279334254",
            },
            {
                uid: uuid.v4(),
                type: "SkillUnlocked",
                title: "Hack 'n Slash",
                description: "Requires Hack 'n Slash.",
                icon: "hack_n_slash.png",
                value: "7cfc22ef-418d-48e1-8e9a-147e65759f66",
            },
            {
                type: "SkillUnlocked",
                title: "Level 7",
                description: "Requires Level 7.",
                icon: "level7.png",
                value: "fde448ce-5fb2-423b-a3b0-f84d9ce8a1b9",
            },
        ],
        data: {
            damage: 15,
            cooldown: 10,
            restore: 10,
        },
    },
];
```

The archetype definition will reference the three root skills of `shield`, `slash` and `heal`. The system will then discover the remaning skills in the archetype automatically.

```javascript
{
    name: "paladin",
    title: "Paladin",
    description: "The Paladin is a holy warrior blessed by the Gods with supernatural strength.",
    icon: "paladin.png",
    skills: [
        "d3f56fd6-9d00-4401-99de-029d5f92d594",
        "c4348f24-5c9e-4d84-a404-fa19aee752bb",
        "0e7bb2e2-b6bb-47b0-b51e-392279334254",
    ],
    data: undefined,
}
```

## Bard Class

The `Bard` is a world-class musician whose songs can heal and uplift even the most tainted of hearts.

The following table illustrates the set of skills that will be awarded at particular levels and their other skill requirements.

| Skill          | Description                                                       | Requires             |
| -------------- | ----------------------------------------------------------------- | -------------------- |
| heal_ballad    | Heal all members of your group for 10 hit points.                 | N/A                  |
| dexterity_song | Increase the dexterity of your entire group by 20 for 30 seconds. | N/A                  |
| heal_song      | Heal all members of your group for 25 hit points.                 | level_5, heal_ballad |

This tree can be encoded into JSON to be created with the service as follows.

```javascript
[
    {
        uid: "82bfd405-26aa-4f33-9293-c4b638f9f7f4",
        dateCreated: new Date(),
        dateModified: new Date(),
        version: 0,
        name: "heal_ballad",
        title: "Ballad of Healing",
        description: "Heal all members of your group for 10 hit points.",
        icon: "heal_ballad.png",
        requirements: [],
        data: {
            restore: 10,
            cooldown: 5,
        },
    },
    {
        uid: "38893137-1200-47dc-a04f-0a01728ac893",
        dateCreated: new Date(),
        dateModified: new Date(),
        version: 0,
        name: "dexterity_song",
        title: "Song of Dexterity",
        description: "Increase the dexterity of your entire group by 20 for 30 seconds.",
        icon: "dexterity_song.png",
        requirements: [],
        data: {
            dexterity: 20,
            cooldown: 1,
            duration: 30,
        },
    },
    {
        uid: "9adc9968-5885-4bac-bb54-d97662e3b22e",
        dateCreated: new Date(),
        dateModified: new Date(),
        version: 0,
        name: "heal_song",
        title: "Song of Healing",
        description: "Heal all members of your group for 25 hit points.",
        icon: "heal_song.png",
        requirements: [
            {
                uid: uuid.v4(),
                type: "SkillUnlocked",
                title: "Ballad of Healing",
                description: "Requires Ballad of Healing.",
                icon: "heal_ballad.png",
                value: "82bfd405-26aa-4f33-9293-c4b638f9f7f4",
            },
            {
                type: "SkillUnlocked",
                title: "Level 5",
                description: "Requires Level 5.",
                icon: "level5.png",
                value: "e53768f4-df1e-497d-8e75-87beebc0cd23",
            },
        ],
        data: {
            restore: 25,
            cooldown: 5,
        },
    },
];
```

The archetype definition will reference the three root skills of `heal_ballad` and `dexterity_song`. The system will then discover the remaning skills in the archetype automatically.

```javascript
{
    name: "bard",
    title: "Bard",
    description:
        "The Bard is a world-class musician whose songs can heal and uplift even the most tainted of hearts.",
    icon: "bard.png",
    skills: ["82bfd405-26aa-4f33-9293-c4b638f9f7f4", "38893137-1200-47dc-a04f-0a01728ac893"],
    data: undefined,
}
```

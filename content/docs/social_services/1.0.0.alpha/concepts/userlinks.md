---
title: "User Links"
date: 2019-07-05T22:50:13.161Z
---

A user link is a relationship of one user to another. A user can have any number of links to any number of other users. Each link describes a relationship from one user to another. This makes it possible to implement the following social network concepts.

-   User Follow
-   Friends
-   Blocked Users

The structure of the UserLink appears as follows:

```javascript
{
    uid: "",
    dateCreated: "",
    dateModified: "",
    version: 0,
    userUid: "",
    otherUid: "",
    type: "FOLLOW"
}
```

## Following Users (`FOLLOW`)

User links with the `FOLLOW` type describes relationships where a user is interested in being following the activity of another user. This relationship is one-way in that the source user (`userUid`) wants to follow the activity other user (`otherUid`). This makes it possible to create loosely coupled relationships between users which can be beneficial when needing to create and maintain a set of one-way relationships for users such as subscribing to a user's feed.

## Friending Users (`FRIEND`)

A user link with the `FRIEND` type is the two-way relationship whereby two users indepedently have chosen to follow the other. As this is a two-way relationship, requiring both users to participate, it is not possible to simply create a user link with the `FRIEND` type. Instead, any time two users create a `FOLLOW` link to each other the system willl automatically upgrade their relationship to a `FRIEND` type. Should either side choose to delete their respective side of the relationship then the opposing link will be downgraded down to a `FOLLOW` link.

For applications implementing a friends list system it is recommended that each user creates a `FOLLOW` link to another and then sends a friend invite message to encourage the other user to create the needed opposite link to complete the `FRIEND` relationship. This can be accomplished via the following steps.

Given user A wants to add user B as a friend...

1. User A creates a UserLink to user B with type `FOLLOW`.
2. User A sends message to user B containing an `invite` attachment to add them as a friend.

```javascript
{
    senderUid: <UserA_UUID>,
    receiverUid: <UserB_UUID>,
    subject: "UserA wants to be your friend!",
    body: "User A wants to be your friend.",
    attachments: {
        invite: "{ type: \"userlink\", userUid: <UserA_UUID> }"
    }
}
```

3. User B receives message containing friend invite sent by User A.
4. User B accepts friend invite. Creates a UserLink to user A with type `FOLLOW`
5. System automatically upgrades both connections to `FRIEND`

## Blocking Users (`BLOCK`)

Not everyone is going to want to be friends. In the event that a user wishes not to interact with another user they can create a UserLink with the `BLOCK` type. This relationship is always a one-way relationship however it is special in that the system will not allow a user to create an opposing `FOLLOW` link if an existing `BLOCK` exists. Similarly, if there exists a `FOLLOW` relationship between the two users then that link will be removed once a `BLOCK` link is created. This is true even in the event that a `FRIEND` relationship exists. In the event that a user attempts to follow a user that has blocked them an error is returned by the service. It is the responsibilty of the application to decide whether or not this error should be displayed to the user.

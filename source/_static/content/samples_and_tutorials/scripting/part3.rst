========================
Managing Data Structures
========================

This is part three of our series on scripting with Xsolla Backend. In part two we discussed how to create new custom REST API endpoints. In part three we will build upon that to create a REST API that serves as a RESTful interface to a custom data structure. Go ahead and open up your test workspace in Visual Studio Code and let’s get started.

In Xsolla Backend, data storage is managed using a strictly typed system of classes that are stored in a database using an Object-Relational Mapping layer (TypeORM). This makes it possible to easily switch between database types based on the different needs of the data structure and service. In fact, it’s possible to have two classes be stored in two entirely different databases within the same service. The ORM framework supports popular SQL databases as well as NoSQL such as MongoDB. Most services in the Xsolla Backend engine have been written to use MongoDB. We will continue that tradition for today’s tutorial.

Let’s imagine that we’re building an RPG in which players can create unique characters (let’s also imagine that Xsolla Backend doesn’t already have a system for this). Each character needs certain attributes stored that matter to our gameplay. Things like health, mana, current equipment and an inventory of items. We’ll start by creating the Character class.

First create a new file called Character.ts. Like routes, it’s recommended practice to place your data structure classes in the models sub-folder.

.. image:: /images/tutorials/scripting/part3_diagram1.png

Now paste the following contents into your file.

.. code-block:: typescript
   :linenos:

   import { Column, Entity, Index } from “typeorm”;
   import { BaseMongoEntity, Cache, Identifier, Model } from “@acceleratxr/service-core”;
   import InventoryItem from “./InventoryItem”;
   
   /**
    * An `Character` is a unique character of a user within the system. Users can have multiple characters per account and the character can have associated data such as inventory, progress, achievements, etc.
    */
   @Cache()
   @Entity()
   @Model(“mongodb”)
   export default class Character extends BaseMongoEntity {
       /**
        * The universally unique identifier of the user that the character belongs to.
        */
       @Column()
       @Index()
       public userUid: string = “”;
   
       /**
        * The unique name of the character.
        */
       @Identifier
       @Index()
       @Column()
       public name: string = “”;
   
       /**
        * A biographical description of the character.
        */
       @Column()
       public biography: string = “”;
   
       /**
        * The amount of health that the character currently has.
        */
       @Column()
       public health: number = 100;
   
       /**
        * The amount of mana that the character currently has.
        */
       @Column()
       public mana: number = 100;
   
       /**
        * A map of the current items the character has equipped. The key is the slot name, the value is the uid to the item
        * that is equipped.
        */
       @Column()
       public equipment: Map<string, string> = new Map();
   
       /**
        * A list all items currently in the character’s possession.
        */
       @Column()
       public inventory: Array<InventoryItem> = [];
   
       /**
        * An arbitrary map of key-value pairs containing the characteristics of the character.
        */
       @Column()
       public attributes: any = undefined;
   
       constructor(other?: any) {
           super(other);
   
           if (other) {
               this.userUid = other.userUid ? other.userUid : this.userUid;
               this.name = other.name ? other.name : this.name;
               this.biography = other.biography ? other.biography : this.biography;
               this.health = other.health ? other.health : this.health;
               this.mana = other.mana ? other.mana : this.mana;
               this.equipment = other.equipment ? other.equipment : this.biography;
               this.inventory = other.inventory ? other.inventory : this.inventory;
               this.attributes = other.attributes ? other.attributes : this.attributes;
           }
       }
   }

The first thing you may notice about this class is that inherits from BaseMongoEntity. The BaseMongoEntity class provides basic information for data that is to be stored in a MongoDB instance. This includes properties such as uid, dataCreated, dateModifed and version. The uid property uniquely identifies the object across all others in the database. The date fields should be self explanatory and the version field is used for optimistic locking. Note that if you were writing for a SQL database you would use the BaseEntityclass instead.

You may also notice the three decorators at the top of the class; @Cache, @Entity and @Model. These are all very important as they tell the server what you intend to do with this class. The @Entity decorator is used to indicate that instances of this class will be stored in a database managed by TypeORM. The @Model decorator is used to identify which database connection that instances of the class should be bound to. In our example, instances of the Character class are bound to the mongodb database connection. Finally, the @Cache decorator tells the server that queries to this class should be cached. Caching speeds up searches for data by storing the results of frequently requested queries in memory. This is also commonly referred to as a Second-Level Cache.

The contents of the class is pretty straight forward. You’ll notice that it is essentially a struct with a simple copy constructor. Each property that will be stored in the database is decorated with @Column. This again tells TypeORM what and how to store instances of the object in the database. The name property also has the @Identifier and @Index decorators. These tell the server that the name property should be indexed in the database (to further speed up queries) and that the property is also a unique identifier (more on this later).

The copy constructor is very simple, it takes an object of type any and then selectively copies all existing values corresponding to properties defined in the class. This serves two purposes. First, it makes converting any arbitrary object to our data type easy. Second, it provides an automatic filtering mechanism, getting rid of any properties we don’t actually care about.

Now that we’ve created our data structure let’s look at how to write a route handler that will allow us to manage it.  Create a new file routes/CharacterRoute.ts and paste the following contents.

.. image:: /images/tutorials/scripting/part3_diagram2.png

.. code-block:: typescript
   :linenos:

   import {
       Auth,
       Config,
       Init,
       Logger,
       Model,
       ModelRoute,
       Repository,
       Delete,
       Get,
       Post,
       Put,
       Param,
       Query,
       Route,
       User as AuthUser,
       AccessControlList,
       ACLRecord,
       Request
   } from “@acceleratxr/service-core”;
   import { JWTUser, UserUtils } from “@acceleratxr/core”;
   import { Request as XRequest } from “express”;
   import Character from “../models/Character”;
   import Count from “../models/Count”;
   import { MongoRepository } from “typeorm”;
   
   /**
    * Handles all REST API requests for the endpoint `/characters`.
    */
   @Model(Character)
   @Route(“/characters”)
   export default class CharacterRoute extends ModelRoute<Character> {
       @Config
       protected config: any;
   
       @Logger
       protected logger: any;
   
       @Repository(Character)
       protected repo?: MongoRepository<Character>;
   
       /**
        * Initializes a new instance with the specified defaults.
        */
       constructor() {
           super();
       }
   
       /**
        * Called by the system on startup to create the default access control list for objects of this type.
        */
       protected getDefaultACL(): AccessControlList | undefined {
           // TODO Customize default ACL for this type
   
           const records: ACLRecord[] = [];
   
           // Anonymous has no access
           records.push({
               userOrRoleId: “anonymous”,
               create: false,
               read: false,
               update: false,
               delete: false,
               special: false,
               full: false,
           });
   
           // Everyone has create/read-only access
           records.push({
               userOrRoleId: “.*”,
               create: true,
               read: true,
               update: false,
               delete: false,
               special: false,
               full: false,
           });
   
           return {
               uid: “Character”,
               dateCreated: new Date(),
               dateModified: new Date(),
               version: 0,
               records,
           };
       }
   
       /**
        * Returns all characters from the system that the user has access to
        */
       @Auth([“jwt”])
       @Get()
       private async findAll(
           @Param() params: any,
           @Query() query: any,
           @AuthUser user?: JWTUser
       ): Promise<Array<Character>> {
           return super.doFindAll(params, query, user);
       }
   
       /**
        * Create a new character.
        */
       @Auth([“jwt”])
       @Post()
       private async create(obj: Character, @Request req: XRequest, @AuthUser user?: JWTUser): Promise<Character> {
           const character: Character = new Character(obj);
   
           // If the userUid was not provided fill it in based on the user
           if (user && (!character.userUid || character.userUid.trim().length === 0)) {
               character.userUid = user.uid;
           }
   
           // A non-admin user cannot create a profile on behalf of someone else
           if (user && character.userUid !== user.uid && !UserUtils.hasRoles(user, this.config.get(“trusted_roles”))) {
               const error: any = new Error(“User does not have permission to perform this action.”);
               error.status = 403;
               throw error;
           }
   
           return super.doCreate(character, user, undefined, true, req);
       }
   
       /**
        * Returns the count of characters
        */
       @Auth([“jwt”])
       @Get(“/count”)
       private async count(@Param() params: any, @Query() query: any, @AuthUser user?: JWTUser): Promise<Count> {
           return super.doCount(params, query, user);
       }
   
       /**
        * Returns a single character from the system that the user has access to
        */
       @Auth([“jwt”])
       @Get(“/:id”)
       private async findById(@Param(“id”) id: string, @AuthUser user?: JWTUser): Promise<Character> {
           return super.doFindById(id, user);
       }
   
       /**
        * Updates a single character
        */
       @Auth([“jwt”])
       @Put(“/:id”)
       private async update(@Param(“id”) id: string, obj: Character, @Request req: XRequest, @AuthUser user?: JWTUser): Promise<Character> {
           const newObj: Character = new Character(obj);
           return super.doUpdate(id, newObj, user, true, req);
       }
   
       /**
        * Deletes the character
        */
       @Auth([“jwt”])
       @Delete(“/:id”)
       private async delete(@Param(“id”) id: string, @Request req: XRequest, @AuthUser user?: JWTUser): Promise<void> {
           return super.doDelete(id, user, true, req);
       }
   }

You may immediately notice a couple things that are different from the route handlers we wrote in part two. First, there is a @Model(Character) decorator in addition to the @Route decorator. This decorator is used to tell the server that this route handler is responsible for managing instances of the Character class. The second thing you may notice is that the class inherits from ModelRoute. The ModelRouteclass is a special base class containing built-in behaviors and utilities for working with data structures. Everything from the basic business logic to handle CRUD operations to automatic permission checking and second level caching is included in this base class. The last major thing you should notice about this route handler is the repo property. The repo property is a reference to the storage interface of the database. The @Repository(Character)decorator tells the server to automatically inject this reference at server start up.

There’s also a new function in this route handler class called getDefaultACL. This function is used to define the base permissions that govern user access to all class level operations (create, count, findAll and truncate). The defaultACL is also used to establish per-document permissions when objects are created using the createoperation. In this example, we are setting the default permissions to allow any logged in user with the ability to create or read records and deny unauthenticated users from performing any operations.

The remainder of the route handler functions follow the common CRUD pattern. The first function, findAll is a search function that accepts query parameters and performs a search against the database for all objects matching the specified criteria. This is easily accomplished by simply calling the doFindAll function in the base class. There are a variety of built-in functions available in the base class described here. The count built-in, for instance, returns the number of results matching the given search criteria.

The create function is a bit different. Here we first create a new Character object using the data that was passed in by the client. This provides that automatic filtering mentioned before. Then we automatically fill in the userUid property with the authenticated user’s if not already provided (for convenience).

When we defined our default permissions above you’ll notice that we allow any authenticated user to create an object. This means that anyone can create a valid Character record with any userUid association. However, since we’re dealing with player characters we want to prevent a player from creating a Character for another player’s account. So we test to make sure that the userUid in the provided character object matches that of the authenticated user. The only exception to this rule is platform super users (such as admins or moderators). We test this by checking to see if the authenticated user has a trusted role.

Finally, we call super.doCreate, passing in the new character object to create as well as the authenticated user. By default the base class will automatically create permissions for the object, inheriting from the default permissions defined above. The authenticated user will also be set with full access for the object as its owner. It is possible to override this behavior by setting the third argument to a custom acl object.

The remaining functions aren’t too complicated as they simply call their corresponding built-in function. The built-in function will automatically take care of all the dirty work when it comes to retrieving objects from the database, validating permissions, caching data and so on.

You may notice that the doUpdate and doFindById handler functions take an id path parameter as the first argument. If you recall from our data structure above we marked certain fields with the @Identifier decorator. When searching for an existing object the system uses these properties to build a special query. This makes it possible to retrieve a character object by either it’s uid or it’s name property all from the same REST API and without requiring multiple lookups.

Go ahead and try for yourself. See what new kinds of REST APIs you can create for your custom data structures. One last thing to note, the order of the function definition does matter. For example, we have count with the path /characters/count in addition to the delete, findById and update functions that each have the path /characters/:id. If the count function were defined at the bottom of the class it wouldn’t work. This is because the :id parameter in the path is a wildcard and so it’ll assume that a request to /characters/count is really a search for a character named count. This is due to the way the underlying web server processes incoming web requests (ExpressJS). So make sure that you define your functions carefully.

In part four we’ll discuss how to create a background job to create automatic time based services.
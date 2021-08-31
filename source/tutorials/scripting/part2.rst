======================
Extending the REST API
======================

Welcome to the second installment of our series on custom scripting using the AcceleratXR Live Scripting System. In part one we covered the AcceleratXR Script Manager and how to create a workspace, sync scripts and work in Visual Studio Code.

This article will focus on extending the platform REST API by creating entirely new endpoints that titles can access to enable custom behavior, new data storage access and more.

AcceleratXR is built upon the open source project ComposerJS. ComposerJS is a generalized framework for creating RESTful API services using NodeJS. One of Composer’s core design principles is to enable rapid development with minimal setup and configuration. As such, each service scans for source code on the running server’s disk, automatically importing and activating that code at startup. This capability dramatically simplifies the development process, reducing the time and difficulty needed to develop the server code. The Live Scripting System has re-imagined this core functionality by pulling source code from a database, in addition to scanning the local disk. Combined this makes it possible to develop all of the source code needed for any kind of new platform functionality without ever having to fork, commit or deploy an AcceleratXR micro-service project directly.

In AcceleratXR there are four primary types of scripts. They are…

* Background Jobs
* Data Models
* Event Handlers
* Route Handlers

This article focuses on the fourth type. A Route Handler is a class decorated with @Route that contains decorated functions capable of processing different kinds of HTTP requests.

For this example we will make a simple route handler that responds to the HTTP request GET /helloworld. To get started open the workspace you created in Part One. Now create a new file and call it HelloWorldRoute.ts. Note it is recommended to place your script in the routes sub-folder.

.. image:: /images/tutorials/scripting/part2_diagram1.png

The first thing we need to do is define the class structure of the route handler. This will look like the following.

.. code-block:: javascript
   :linenos:

   import { RouteDecorators } from “@acceleratxr/service-core”;
   const {
       Route,
   } = RouteDecorators;

   @Route(“/helloworld”)
   export default class HelloWorldRoute {
   }

Next we need to define the actual handler function that will process GET requests. This is done by creating any function with the @GET decorator.

.. code-block:: javascript
   :linenos:

   import { RouteDecorators } from “@acceleratxr/service-core”;
   const {
       Get,
       Route,
   } = RouteDecorators;

   @Route(“/helloworld”)
   export default class HelloWorldRoute {   
       @Get()
       getHelloWorld(): string {
           return “Hello World!”;
       }
   }

In the above example you’ll notice that we return a string as the function result. This string will be output to the end client in a JSON encoded format. Go ahead and save the script, then publish it to activate. Once published you can access the new endpoint immediately from your browser.

.. image:: /images/tutorials/scripting/part2_diagram2.png

Congratulations! You’ve just created your first new REST API endpoint in AcceleratXR. Now let’s try something a bit more complicated. What if we want to greet the user instead, based on an id passed in via a URL parameter. Let’s say something like GET /hello/sam. We can do this by modifying our route handler as follows.

.. code-block:: javascript
   :linenos:

   import {
       RouteDecorators
   } from “@acceleratxr/service-core”;
   const {
       Get,
       Param,
       Route,
   } = RouteDecorators;
   
   @Route(“/hello”)
   export default class HelloWorldRoute {
       @Get(“/:id”)
       getHelloWorld(@Param(“id”) id: string): string {
           return `Hello ${id}!`;
       }
   }

The first thing to notice is that we changed the path from /helloworld to just /hello at the class level. This tells the server that this route handler will handle all requests starting with the path /hello. Second, we’ve added a sub-path to the @GET decorate /:id. The :id tells the server that this is a parameterized path. Lastly, we’ve also added a single function argument, id with the decorator @Param. This tells the server that it needs to parse the request path for a parameter of the given name, id, and pass the value as an argument to this function. Now we return a new string containing the passed in name from the request path. Save and publish your script again and try it in your browser.

.. image:: /images/tutorials/scripting/part2_diagram3.png

The next thing you may be wondering is how you identify users making requests. This is as simple as adding a new function parameter decorated with @User. For example, let’s create a new function that uses the authenticated user’s first name instead.

.. code-block:: javascript
   :linenos:

   import {
       RouteDecorators
   } from “@acceleratxr/service-core”;
   const {
       Get,
       Param,
       Route,
       User,
   } = RouteDecorators;
   
   @Route(“/hello”)
   export default class HelloWorldRoute {
       @Get(“/:id”)
       getHelloWorld(@Param(“id”) id: string): string {
           return `Hello ${id}!`;
       }
   
       @Get()
       getHelloUser(@User user?: any): string {
           if (user && user.firstName) {
               return `Hello ${user.firstName}!`;
           } else {
               return “Hello Guest!”;
           }
       }
   }

The new function, called getHelloUser, has a single parameter for the authenticated user. We are expecting that the authenticated user has a property firstName that we can use to display in the response (although this is not guaranteed). If a user is not authenticated we simply call them Guest. Let’s try this one in the browser with no authentication.

.. image:: /images/tutorials/scripting/part2_diagram4.png

Next let’s try it with an authenticated user. We’ll pass in the authentication token using the jwt_token query parameter.

.. image:: /images/tutorials/scripting/part2_diagram5.png

The last item we’ll cover here is how to deal with a content body. This is handled pretty simply by adding a single argument to the function parameter of type any. Since ComposerJS is a JSON based framework, HTTP requests that send in JSON objects will already be parsed once passed into the function, saving you time and difficulty. Similarly, if you return an object back from your route handler function the server will automatically encode the result as JSON when returning to the client.

.. code-block:: javascript
   :linenos:

   import {
       RouteDecorators
   } from “@acceleratxr/service-core”;
   const {
       Get,
       Param,
       Post,
       Route,
       User,
   } = RouteDecorators;
   
   @Route(“/hello”)
   export default class HelloWorldRoute {
       @Get(“/:id”)
       getHelloWorld(@Param(“id”) id: string): string {
           return `Hello ${id}!`;
       }
       @Get()
       getHelloUser(@User user?: any): string {
           if (user && user.firstName) {
               return `Hello ${user.firstName}!`;
           } else {
               return “Hello Guest!”;
           }
       }
       @Post()
       postMessage(obj: any): any {
           return obj;
       }
   }

In our above example we’ve defined a new function, postMessage, that handles requests of type POST. It expects a content body that will be parsed as the objargument which will then be returned as the response. Since we know the server will encode objects for us we expect our response to be encoded in JSON.

Since we can’t easily send a POST request using a browser we’ll try this one out using the curl command line utility.

.. image:: /images/tutorials/scripting/part2_diagram6.png

You’ll notice that we sent a JSON encoded string and received a properly formatted JSON string in return. We could alternatively modify the code to return only the msg portion of the object and we’d get back a string like in the previous examples.

Now that we’ve gone over all the basics make sure to read more about all the different ways you can construct route handlers on the ComposerJS website.

In part three we’ll discuss creating data models and how to expose simple CRUD access between the database and a custom REST API.
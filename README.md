# Events-Library
These library aims to provide a common interface for sending and receiving events in our microservice architecture, abstracting all microservices from implementation details such as:

- retry logic of events in certain scenarios
- logging of events (for tracing bugs and failures)
- the transport layer (HTTP, TPC, etc.)
- the event bus/message broker (Kakfa, RabbitMQ, Redis, etc.)


## Requirements
- Python 3.7
- Django
- Django REST Framework

## Usage

The library exposes two main methods:
- **emit** (*event_type*: `str`, *payload*: `dict`)
- **subscribe_to** (*event_type*: `str`, *event_handler*: `funtion`)

The following sections will show their usage
	    
## Subscribing to event

**1 - Declare event handlers**

The event handler is just a funcion that receives a single argument: the payload of the event.
So, in some file (let's call it **event_handlers.py**), you would simply do :

    def handle_user_created(payload):
	    user_id = payload['user_id']
	    email = payload['email']
	    User.objects.create(id=user_id, email=email)

    def handle_user_deleted(payload):
        user_id = payload['user_id`]
        User.objects.filter(id=user_id).delete()


**2 - Import the `subscribe` function and use it**

The subscription to an event should happen as soon as the server starts running. That's why you must do this step in the **config file** (app.py) of your app:

    from events_library import subscribe_to 
    from .event_handlers import handle_user_created, handle_user_deleted
    
    class MyAppConfig(AppConfig):
	    name = 'my_app'
	    
	    def ready(self):
		    subscribe_to('user-created', handle_user_created)
		    subscribe_to('user-deleted', handle_user_deleted)
		    
Of couse, in another app (in the same Service), your could subscribe to those same events (and others) using another event handlers:

**event_handler.py**

    def handle_user_created(payload):
	    user_id = payload['user_id']		
	    customer = ChargebeeCustomer.objects.create(user_id=user_id)
	    ChargebeeCustomerSubscription.objects.filter(customer=customer)

    def handle_user_deleted(payload):
        user_id = payload['user_id']
	    ChargebeeCustomer.objects.filter(user_id=user_id).delete()
	    ChargebeeCustomerSubscription.objects.filter(user_id=user_id).delete()

	def handle_user_updated(payload):
		email = payload['email']
		send_email(to=email, subject="Hello updated user")

**app.py**

    from events_library import subscribe_to 
    from .event_handlers import (
        handle_user_created, 
        handle_user_deleted,
        handler_user_updated,
    )
    
    class MySecondAppConfig(AppConfig):
	    name = 'my_second_app'
	    
	    def ready(self):
		    subscribe_to('user-created', handle_user_created)
		    subscribe_to('user-deleted', handle_user_deleted)
		    subscribe_to('user-deleted', handler_user_updated)

##  Emiting Events

Is as simple as importing the `emit` function from the library and call it using the appropiate `event_type` and `payload` arguments.
 		
	import emit fromt events_library

    def some_function(*args, **kwargs):
        # Some custom code logic before emiting the event
        
        emit('user_created', {
	        'user_id': user.id,
	        'email': user.email,
	    })
	    
        # Some custom code logic after emiting the event

The library will handle any exception that might occur while emiting the event, so there's no need for `try/except` blocks everytime you use the `emit` function.

Of course, you can broadcast in a row as many events as you'd like:

    import emit fromt events_library	
	
    def emit_all_events(*args, **kwargs):
	    # These are good
        emit('profile_created', {'user_id': 1, 'email': 'example_1@gmail.com'})        
        emit('profile_created', {'user_id': 2, 'email': 'example_2@gmail.com'})
        emit('profile_created', {'user_id': 3, 'email': 'example_3@gmail.com'})        


## Philosophy

These are some assumptions that were made while building the library:

 1. There is a single instance of each service in the network
 3.  Whenever event A is emitted, this event should always reach all services that are subscribed to event A
 4. Whenever event  A is emitted, the payload sent along that event follows always a concrete structure:
 5. The library knows nothing about the payloads that are associated to each event type, so it will not raise any validations errors: **Is your responsability to provide the correct payload each time you emit an event**

All these considerations means that the library expects that developers count with a public API or document, which contains all the information related to each kind of event, which should include:

 - name of the event
 - structure of the payload sent along that event
 - who emits each event
 - which services are subscribed to that event

Also, as a guideline, we think is better if an event is emitted from a single responsable service (event **A** is either emitted for service **B** or **C**, but not from both), but the library does not enforce this condition at any level

## Implementation Details

Here we mention details about the current implementation of the library, which might be subject to changes in the near future: this section will be modified when that happens.

**1- The services sends events directly to one another**
This means that currently, there is not a third party service that acts as a proxy/intermediary for sending the event from service A to service B, and viceversa
 
**2- The library uses HTTP  as transfer protocol**
This means that we keep a request/response mechanism, so please keep in mid that **the execution of the code that goes after a call to the `emit` function might be delayed because of network traffic, failures and retries**.

**3- Subscribe depends on devops configuration** 

The `subscribe_to` function does not make a **real** subscriptionall it does is attach the `handler_function` argument to a `ViewSet` that is configured locally by the library.

Then, the **devops** submodule, who is included in all services, imports that viewset and registers it at a specified route, in the urls.py file of the project.

The actual subscription resides in a config object, which is also set by the **devops** sub-module, and that is used internally by the library.

Summing up, this means that:

- if there are events **A** and **D**
- if service **B** called the `subscribed_to` function with **A** as argument
- if service **C** called the `subscribed_to` function with **A** as argument
- in the deveop settings, we have this mapping:  **{ 'A': ['C'] , 'D': ['B', 'C'] }**

Then:
- if the event **A** is emitted, it will be received and handled by service **C** but it will not be received by service **B**. 
- if the event **D** is emited, it will be received by both services **B** and **C**, but it will also not be handled in both cases. This will not raise any errors, but it means that we could simply not sent that event to services **B** and **C**.

So, the configuration file, defined in the `devops` submodule, should be optimal and flawless. In the future we will be able to get rid off this configuration and make thinks in a better way.


**4 - No more REST**

Internally, we are using a single endpoint, which receives **POST** requests.  The body of the request contains two params:`event_type` and `payload`, which are used to call the appropiate event handlers.

We decided to go for this approach because it allows to implement the `emit`and `subscribe_to`functions with the same signature as the ones that are commonly used in sophisticated message brokers.

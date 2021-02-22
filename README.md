# Events-Library

This library aims to provide a common interface for sending and receiving events in our microservice architecture, abstracting all microservices from implementation details such as:

- retry logic of events in certain scenarios
- logging of events (for tracking bugs and issues)
- the transport layer (HTTP, TPC, etc.)
- the event bus or message broker (Kakfa, RabbitMQ, Redis, etc.)

## Requirements

- Python 3.7
- Django
- Django REST Framework

## Usage

The library exposes for the clients two methods:

- **emit** (_event_type_: `str`, _payload_: `dict`)
- **subscribe_to** (_event_type_: `str`, _event_handler_: `funtion`)

That's all you need to use it. The following sections will show their usage

## Subscribing to events

**1 - Declare event handlers**

The event handler is just a funcion that receives a single argument: the payload that
was sent along the event.

So, in some file (let's call it **event_handlers.py**), you would simply do :

    def handle_user_created(payload):
        user_id = payload['user_id']
        email = payload['email']
        User.objects.create(id=user_id, email=email)

    def handle_user_deleted(payload):
        user_id = payload['user_id`]
        User.objects.filter(id=user_id).delete()

**2 - Import the `subscribe_to` function and use it**

The subscription to an event should happen as soon as the server starts running.
That's why you must do this step in the **config file** (app.py) of your app:

    from events_library import subscribe_to
    from .event_handlers import handle_user_created, handle_user_deleted

    class MyAppConfig(AppConfig):
        name = 'my_app'

        def ready(self):
    	    subscribe_to('user-created', handle_user_created)
    	    subscribe_to('user-deleted', handle_user_deleted)

Of couse, in another app (in the same Service), you could subscribe to those same events (and others) using other event handlers:

**event_handler.py**

    def handle_user_created(payload):
        user_id = payload['user_id']
        customer = ChargebeeCustomer.objects.create(user_id=user_id)
        ChargebeeCustomerSubscription.objects.filter(customer=customer)

    def handle_user_deleted(payload):
        user_id = payload['user_id']
        ChargebeeCustomer.objects.filter(user_id=user_id).delete()

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

## Emiting Events

You only need to import the `emit` function from the library and call it using the appropiate `event_type` and `payload` arguments.
import emit from events_library

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
        emit('profile_created', {'user_id': 1, 'email': 'example_1@gmail.com'})
        emit('profile_created', {'user_id': 2, 'email': 'example_2@gmail.com'})
        emit('profile_created', {'user_id': 3, 'email': 'example_3@gmail.com'})

## Philosophy

These are some assumptions that were made while building the library:

1.  There is a single instance of each service in the network
2.  The service that emits an event knows nothing about which services are subscribed to that event
3.  Whenever event A is emitted, the payload sent along that event always has the same structure
4.  The library should know nothing about the payloads that are associated to each event type, so it will not raise any validations errors: **Is your responsability to provide the correct payload each time you emit an event**

All these considerations mean that the library expects that developers count with a public API or document, which contains all the information related to each kind of event, which should include:

- name of the event
- structure of the payload sent along that event
- who emits each event
- which services are subscribed to that event

Also, as a guideline, we think is better if an event is emitted from a single responsable service (event **A** is either emitted for service **B** or **C**, but not from both), but the library does not enforce this condition at any level.

## Implementation Details

Here we mention details about the current implementation of the library, which might be subject to changes in the near future: this section will be modified when that happens.

**1- The services sends events directly to one another**
This means that currently, there is not a third party service that acts as a proxy/intermediary for sending the event from service A to service B, and viceversa

**2- The library uses HTTP as transfer protocol**
This means that we keep a request/response mechanism, so please keep in mind that **the execution of the code that goes after a call to the `emit` function might be delayed because of network traffic, failures and retries**.

**3- Subscribe depends on devops configuration**

The `subscribe_to` function does not make a **real subscription**: all it does is attach the `handler_function` argument to a `ViewSet` that is configured locally by the library.

Then, the **devops** submodule, who is included in all services, imports that viewset and registers it at a specified route, in the urls.py file of the project.

The actual subscription resides in a config object, which is also set by the **devops** submodule, and that is used internally by the library.

Summing up, this means that:

- if there are events **A** and **D**
- if service **B** called the `subscribed_to` function with **A** as argument
- if service **C** called the `subscribed_to` function with **A** as argument
- in the deveop settings, we have this mapping: **{ 'A': ['C'] , 'D': ['B', 'C'] }**

Then:

- if the event **A** is emitted, it will be received and handled by service **C** but it will not be received by service **B**.
- if the event **D** is emited, it will be received by both services **B** and **C**, but it will not be handled by any of them. This will not raise any errors, but it means that we are better off avoiding sending that event to services **B** and **C**.

So, the configuration file, defined in the `devops` submodule, should be optimal and flawless. In the future we will be able to get rid off this configuration and make things work in a better way.

**4 - No more REST**

Internally, we are using a single endpoint, which receives **POST** requests. The body of the request contains two params: `event_type` and `payload`, which are used to call the appropiate event handlers.

We decided to go with this approach because it allows to implement the `emit`and `subscribe_to` functions with the same signature as the ones that are commonly used in sophisticated message brokers.

## Give us your Feedback

We are still figuring out the best way to implement the library: so, if you have some thoughts about how to improve the library in any way, please share it on the dev channel
in Slack.

Here are some ideas we considered while thinking about how to build the library: you're welcome to use them as a starting point for any suggestion you could provide.

**1- Location of the config file**

Instead of having the configuration for subscriptions (mapping between event and target services) in the devops submodule settings file, we could export from the events_library a `declare_event` function that allows to edit this configuration: this means each service, in each of their apps, could do in the app.py file something like this:

    class MyAppConfig(AppConfig):
        name = 'my_app'

        def ready(self):
            declare_event('user_createad', ['payments', 'selfdecode', 'orders'])
            declare_event('user-deleted', ['payments', 'selfdecode'])

We decided not to use this approach because once we use an **actual event bus**, we will have to remove those lines from each service (instead of removing them from a single place). Also, because this approach breaks the principle: _the service that emits an event should know nothing about the services that are subscribed to that same event_ (for this same reason we decided not to put that config in the library itself)

**2- Create an event service**

So, the basic idea was to create a service **E**, known by any other service, that would handle the communication between microservices. How would this work?

Well, when a service **A** starts running, it would send a request to service **E**, saying something like: _"Hey, I wanna subscribe to events **X**, **Y** and **Z**: so please send those to me whenever they are emitted"_. This is basically the **subscription phase**: **E** would store this information in RAM.

Now, when a service **B** calls the `emit` function with **Y** as `event_type`, it would send a request to **E** with the `event_type` and the `payload`, and then, based on the information previously collected, **E** would send (forward) that same request to **A**.

This way, no service will know anything about each other, and we wouldn't need to store statically the information about which service is subscribe to which events.

However, this is a classic bottleneck situation (all network traffic going both ways through a single node), so we thought about the idea of making the requests go directly from service **B** to service **A**.

To do that, when service **B** starts running, it would send a request to **E** saying something like: _"Hey, I emit the event **Y**: give me the list of services that are subscribed to that event"_. Then service **B** would store that information locally in RAM, and whenever it emits an event **Y**, it already knows to which services the event should be sent, so the request could be done directly to service **A** in this case, avoiding the role of **E** as a proxy.

However, this approach has some drawbacks. For example:

**- No easy way to unsubscribe from an event**

Ideally, **A** should never have to call an `unsubscribe_from` function, using **Y** as `event_type` argument: if **A** didn't call the `subscribe_to` function when it started running again (after deleting the `subscribe_to` call), then it is not subscribed to such event. That should be it.

However, this wouldn't work with the implementation explained above, because the information about **A** being subscribed to **Y** would still live in both services **E** and **B**: it would required to reboot again those services, or add custom logic for allowing the _"unsubscription"_.

**- Hard to synchronize on common scenarios**
If a third service **C**, who started running after **B**, subscribes to event **Y**, then service **B** would not know about that and it would never send the event to **C**.
This would require to make the current flow a little more complex, by doing something like this when service **C** starts running:

_"Hey service **E**! I, service **C**, want to subscribe to event **Y**, so please also inform that to the service which emits that event"_

But what if service **E** was rebooted after a rebuild? Then the information about **C** being subscribed to event **Y** would be deleted, and if **B** was to be rebooted later, then it would no be notified about the existance of **C**.

**3- Use Event classes**

    class Event(models.Model):
        id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

        class Meta:
            abstract = True

    class DeleteUserEvent(Event):
        user_id = models.UUIDField()

    class CreateUserEvent(DeleteUserEvent):
        email = models.EmailField()

Having something like that would allow to use classes instead of raw strings when emitting/subscribing events: this would help with validation, and also with the logging of errors in database (instead of storing the event's payload as a JSON field, we could store independent columns for each field in the payload).

The bad thing about this approach is that the library would need to know before hand which are the different events that might be emitted, which goes against the principle of being event-agnostic.

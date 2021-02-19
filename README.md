# Events-Library
These library aims to provide a common interface for sending and receiving events in our microservice architecture, abstracting all microservices from implementation details such as:

- retry logic of events in certain scenarios
- logging of events (for tracing bugs and failures)
- the transport layer (HTTPS, sockets)
- the message broker (Kakfa, RabbitMQ or other)


## Requirements
- Python 3.7
- Django
- Django REST Framework

## Implementation

The library exposes two main methods:
- **emit** (*event_type*: `str`, *payload*: `dict`)
- **subscribe_to** (*event_type*: `str`, *event_handler*: `funtion`)
- **declare_event** (*event_type*: `str`, *target_services*: `List[str]`)


## Philosophy and Implementation
These are some assumptions that were made while building the library:
 1. There is a single instance of each service in the network
 2.  Whenever event **A** is emitted, this event should always reach all services that are subscribed to event **A**
 3. Whenever event **A** is emitted, the payload sent along that event follows a same structure


##  Emiting Events

Whenever you want to emit some event, this is what you should do:

**1- Declare the event in you app config file**
Under the **2nd** assumption mentioned in the section above, there's no need to declare which are the target services each time an event is emited. So doing it a single time, when the service starts running, should be enough.

So, for example, in a **user** app in your service, you would do as in the next example:

    from django.apps import AppConfig
    from common.events import Event
    
    from events_library import declare_event, Service
    
    class  UserConfig(AppConfig):
	    name = 'user'
	    
	    def ready(self):
		    declare_event('user-created',[Service.PAYMENT, Service.ORDERS])
		    declare_event('user-deleted',[Service.PAYMENT])

List item

**2- Import the `emit` function from the library**
**3 - Call the emit function using the appropiate `event_type` and `payload`**
 
**Example:**
		
	import emit fromt events_library

    def some_function(*args, **kwargs):
        # Some custom code logic before emiting the event
        
        emit('user_created', {
	        'user_id': user.id,
	        'email': user.email,
	    })
	    
        # Some custom code logic after emiting the event

The library will handle any exception that might occurr while emiting the event, so there's no need for `try/except` blocks everytime you use the `emit` function.

Of course, you can emit as many events as you'd like in a row

    import emit fromt events_library	
	
    def emit_all_events(*args, **kwargs):	    
        emit('profile_created', {'user_id': 1})
        emit('profile_created', {'user_id': 2})
        emit('profile_created', {'user_id': 3})
        emit('profile_created', {'user_id': 4})
	    
	    
## Subscribing to event

In the same way, if you want to subscribe to an event, you should do that in the config file **app.py** on each of your apps

    import emit fromt events_library

	@subscribe_to('user-create')
	def handle_user_created(event_data):
	    user_id = event_data['user_id']
	    email = event_data['email']
	    User.objects.create(id=user_id, email=email)

Notice that you can subscribe as many event_handlers `event_type` in different places of your code, ensuring that all required actions are performed by following the Single Responsability Principle (SRP).

This is 
	

	# apps/chargebee
    @subscribe_to('user-deleted')
    def handle_user_deleted_B(event_data):
        user_id = event_data['user_id']
    
	    ChargebeeCustomer.objects.filter(user_id=user_id).delete()
	    ChargebeeCustomerSubscription.objects.filter(user_id=user_id).delete()


	apps/chargebee
    @subscribe_to('user-deleted')
    def handle_user_deleted_B(event_data):
        user_id = event_data['user_id']
    
	    ChargebeeCustomer.objects.filter(user_id=user_id).delete()
	    ChargebeeCustomerSubscription.objects.filter(user_id=user_id).delete()



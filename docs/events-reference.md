
## Create an User in Accounts

This event is emitted when a user is created in the Account's Service. The
creation should propagate to other's services that keeps a replica of the 
User table.

**Sent From**: Account's Service   
**Sent To**: Payment's Service, SelfDecode

    event_type: "user-create"

    payload:
       	uuid: uuid
		The id of the user in Account's Service

	email: string
		The email of the user. This field is unique
		among users in Account's Service

	token: string
		Used for generating a link for recovery
		of lost credentials

	token_for_email: string
		Used for generating a link for recovery
		of lost credentials

## Update an User in Accounts
This event is emitted when an user is updated in the Account's Service: the only fields that can be updated for the user are the email and password, but password lives only in the Account's Service, so only the edition of the email field should propagate to other's services that keeps a replica of the User table

**Sent From**: Account's Service
**Sent To**: Payment's Service, SelfDecode

    event_type: "user-update"
    
    payload:
    	uuid: uuid
		The id of the user in Account's Service

    	email: string
		The email of the user. This field is unique
		among users in Account's Service

# Delete an User in Accounts

This event is emitted when an user is deleted from the Account's Service. The deletion should propagate to other's services that keeps a replica of the User table

**Sent From**: Account's Service
**Sent To**: Payment's Service, SelfDecode

    event_type: "user-delete"
    
    payload:
    	uuid: uuid
		The id of the user in Account's Service

## Payment of an Order

Short description about this event. What does it does? When should it be emmited? 

**Sent From**: Payment's Service
**Sent To**: Order's Service

    event_type: "order-paid"
    
    payload:
    	order_id: uuid
		The id of the order in the Order's Service
    	
    	shipping_location: string
    		The name of the country to which the 
		order is being sent. The values come
		from the django_countries package

## User Report Count
Short description about this event. What does it does? When should it be emmited?

**Sent From**: Payment's Service
**Sent To**: SelfDecode

    event_type: "user-report-count"
    
    payload:
    	user_id: uuid
    		The id of the user in Account's Service
    	
    	count: int
    		The amount of reports purchased by the
    		user so far
    	
    	report_type: string
    		The type of the recently purchased report.
    		Possible values are: 'any' | ...


## User Profile Count
Short description about this event. What does it does? When should it be emmited?

**Sent From**: Payment's Service
**Sent To**: Profile's Service

    event_type: "user-profile-count"
    
    payload:
    	user_id: uuid
    		The id of the user in Account's Service
    
    	profile_count: int
    		The amount of profiles the user currently has

## Create UserSubscription
Short description about this event. What does it does? When should it be emmited?

**Sent From**: Payment's Service
**Sent To**: Profile's Service

    event_type: "user-subscription-create"
    
    payload:
    	user_id: uuid
    		The id of the user in Account's Service
    
    	subscription_id: uuid
    		The id of the UserSubscription in Payment's Service
    
    	plan: string
    		A string, which represents the plan of
    		the subscription. Possible values are:
    		"free" | "standard" | "professional"

## Payment of Practitioner's Order
Short description about this event. What does it does? When should it be emmited?

**Sent from**: Order's Service
**Sent To**: Payment's Service	

    event_type: "practitioner-payment"
    
    payload:
    	user_id: uuid
    		The id of the user in the Account's Service
    
    	order_id: uuid
    		The id of the order in the Order's Service
    
    	shipping_location: string
    		The name of the country to which
    		the order is being sent. The values come
    		from the django_countries package

## Create a profile in Profile's Service
Short description about this event. What does it does? When should it be emmited?

**Sent From**: Profile's Service
**Sent To**: Genome File's Service, SelfDecode

    event_type: "profile-create"
    
    payload:
    	id: uuid
    		The id of the profile in Profile's Service
    
    	timestamp: string
    		The date in which the profile was created,
    		in ISO format
    
    	data: dict
    		The fields needed for creating the profile
    		--->HERE WE SHOULD GIVE MORE DETAILS ABOUT
    		THE COMPOSITION OF THE DATA DICT, WHICH I
    		ASSUME IS GENDER, ETHNICITY, ETC    <--

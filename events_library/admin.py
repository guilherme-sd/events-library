from django.contrib import admin
from events_library.models import EventLog, HandlerLog

# Register your models here.
admin.site.register(EventLog)
admin.site.register(HandlerLog)

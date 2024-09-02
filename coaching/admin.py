from django.contrib import admin
from .models import Event,Participant,Payment
# Register your models here.
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Payment)

from django.contrib import admin

from home.models import Person, Transaction

# Register your models here.
admin.site.register(Person)
admin.site.register(Transaction)

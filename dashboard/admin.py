from django.contrib import admin
from dashboard.models import AiUser, Property, Unit, Tenant, Lease
from django.contrib.auth.models import Group

# Register your models here.

admin.site.unregister(Group),
admin.site.register(AiUser),
admin.site.register(Property),
admin.site.register(Unit),
admin.site.register(Tenant),
admin.site.register(Lease),

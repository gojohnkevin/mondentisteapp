from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from provider.oauth2.models import Client

from accounts.models import (
    DeviceToken,
    Photo,
    DentistDetail,
    Appointment,
    EmergencySchedule,
)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'dentist', 'status')


admin.site.register(DeviceToken)
admin.site.register(Photo)
admin.site.register(DentistDetail)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(EmergencySchedule)

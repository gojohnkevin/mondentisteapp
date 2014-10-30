from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from provider.oauth2.models import Client

from accounts.models import (
    DeviceToken,
    Photo,
    DentistProfile,
    Appointment,
    EmergencySchedule,
    Notification,
    Book,
    UserProfile,
    Note,
)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient', 'dentist', 'status')

    def get_patient(self, obj):
        return obj.patient.profile.name
    get_patient.short_description = 'Patient'

class PhotoAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'dentist':
            kwargs['initial'] = request.user.id
        return super(PhotoAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def queryset(self, request):
        qs = super(PhotoAdmin, self).queryset(request)
        return qs.filter(dentist=request.user)


class EmergencyScheduleAdmin(admin.ModelAdmin):
    list_display = ('dentist', 'date', 'time',)


admin.site.register(DeviceToken)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(DentistProfile)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(EmergencySchedule, EmergencyScheduleAdmin)
admin.site.register(Notification)
admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Note)
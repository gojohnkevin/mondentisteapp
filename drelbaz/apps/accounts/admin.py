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
    Notification,
    Book,
)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'dentist', 'status')

class PhotoAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(PhotoAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def queryset(self, request):
        qs = super(PhotoAdmin, self).queryset(request)
        return qs.filter(user=request.user)


class EmergencyScheduleAdmin(admin.ModelAdmin):
    list_display = ('dentist', 'date', 'time',)


admin.site.register(DeviceToken)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(DentistDetail)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(EmergencySchedule, EmergencyScheduleAdmin)
admin.site.register(Notification)
admin.site.register(Book)

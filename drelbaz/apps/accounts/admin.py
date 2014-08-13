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


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('first_name', 'last_name', 'email',)
    actions = ('generate_api_key',)

    def generate_api_key(self, request, queryset):
        rows_updated = 0
        for obj in queryset:
            try:
                site = Site.objects.get(id=1)
                c = Client(user=obj, name=obj.get_full_name(), client_type=0, url=site.domain)
                c.save()
                rows_updated += 1
            except Exception as e:
                print e
                self.message_user(request, '%s had a problem generating api key. (%s).' % (obj, str(e),))
            self.message_user(request, '%s users successfully generated api key.' % rows_updated)

    generate_api_key.short_description = "Generate API Key"


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'dentist', 'status')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(DeviceToken)
admin.site.register(Photo)
admin.site.register(DentistDetail)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(EmergencySchedule)

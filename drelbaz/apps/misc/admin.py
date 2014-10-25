from django.contrib import admin

# Register your models here.
from misc.models import (
    DentalClinic,
    Blog,
)


admin.site.register(DentalClinic)
admin.site.register(Blog)
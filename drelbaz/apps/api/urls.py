from django.conf.urls import patterns, include, url

from tastypie.api import Api
from .api import (
    DeviceTokenResource,
    PhotoResource,
    UserResource,
    DentistDetailResource,
    AppointmentResource,
    EmergencyScheduleResource,
)

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(DeviceTokenResource())
v1_api.register(PhotoResource())
v1_api.register(DentistDetailResource())
v1_api.register(AppointmentResource())
v1_api.register(EmergencyScheduleResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)

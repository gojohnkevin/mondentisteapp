from django.conf.urls import patterns, include, url

from tastypie.api import Api
from .api import (
    PhotoResource,
    UserResource,
    DentistDetailResource,
    AppointmentResource,
)

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(PhotoResource())
v1_api.register(DentistDetailResource())
v1_api.register(AppointmentResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)

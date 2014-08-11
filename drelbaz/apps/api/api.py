from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf.urls import url

from authentication import OAuth20Authentication
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import (
    ModelResource,
    ALL, ALL_WITH_RELATIONS
)
from tastypie.utils import trailing_slash
from tastypie.validation import FormValidation


from .validation import ModelFormValidation
from accounts.models import (
    DeviceToken,
    Photo,
    DentistDetail,
    Appointment
)
from accounts.forms import (
    AppointmentForm,
    DentistDetailForm,
    DeviceTokenForm,
)


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email', 'username',]
        allowed_methods = ['get', 'post',]
        resource_name = 'user'
        authentication = OAuth20Authentication()
        filtering = {
            'username': ['exact',],
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)


class DeviceTokenResource(ModelResource):
    class Meta:
        queryset = DeviceToken.objects.all()
        resource_name = 'devicetoken'
        allowed_methods = ['get', 'post',]
        #authentication = OAuth20Authentication()
        authorization = DjangoAuthorization()
        validation = FormValidation(form_class=DeviceTokenForm)


class PhotoResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Photo.objects.all()
        resource_name = 'photo'
        allowed_methods = ['get', 'post',]
        authentication = OAuth20Authentication()
        authorization = DjangoAuthorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }


class DentistDetailResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = DentistDetail.objects.all()
        resource_name = 'dentistdetail'
        allowed_methods = ['get', 'post', 'patch', 'put',]
        authentication = OAuth20Authentication()
        authorization = DjangoAuthorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }
        validation = FormValidation(form_class=DentistDetailForm)


class AppointmentResource(ModelResource):
    dentist = fields.ForeignKey(UserResource, 'dentist')

    class Meta:
        queryset = Appointment.objects.all()
        resources = 'appointment'
        allowed_methods = ['get', 'post',]
        authentication = OAuth20Authentication()
        authorization = DjangoAuthorization()
        validation = ModelFormValidation(form_class=AppointmentForm)

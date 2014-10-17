import json

from collections import OrderedDict
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.conf.urls import url
from django.core.serializers.json import DjangoJSONEncoder

from authentication import OAuth20Authentication
from provider.oauth2.models import Client
from tastypie.authentication import (
    Authentication, ApiKeyAuthentication, BasicAuthentication,
    MultiAuthentication
)
from tastypie import fields
from tastypie.authorization import (
    Authorization,
    DjangoAuthorization
)
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.resources import (
    ModelResource,
    ALL, ALL_WITH_RELATIONS
)
from tastypie.utils import trailing_slash
from tastypie.validation import FormValidation

from .exceptions import CustomBadRequest
from .utils import (
    MINIMUM_PASSWORD_LENGTH,
    validate_password,
    retrieve_oauth_client
)
from .validation import ModelFormValidation
from accounts.forms import (
    AppointmentForm,
    DentistProfileForm,
    DeviceTokenForm,
    EmergencyScheduleForm,
)
from accounts.models import (
    DeviceToken,
    Photo,
    DentistProfile,
    Appointment,
    EmergencySchedule,
    Notification,
    Book,
    UserProfile,
)

optional = {
    'null' : True,
    'blank': True,
}


class UserResource(ModelResource):
    raw_password = fields.CharField(attribute=None, readonly=True, null=True,
                                    blank=True)

    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email', 'username',]
        allowed_methods = ['get', 'post', 'patch',]
        resource_name = 'user'
        authentication = OAuth20Authentication()
        authorization = Authorization()
        filtering = {
            'username': ['exact',],
        }

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()

    def hydrate(self, bundle):
        if 'raw_password' in bundle.data:
            raw_password = bundle.data.pop('raw_password')

            if not validate_password(raw_password):
                if len(raw_password) < MINIMUM_PASSWORD_LENGTH:
                    raise CustomBadRequest(
                        code='invalid_password',
                        message=(
                            'Your password should contain at least {length} '
                            'characters.'.format(length=
                                                 MINIMUM_PASSWORD_LENGTH)))
                raise CustomBadRequest(
                    code='invalid_password',
                    message=('Your password should contain at least one number'
                             ', one uppercase letter, one special character,'
                             ' and no spaces.'))

            bundle.obj.set_password(raw_password)
        return bundle

    def dehydrate(self, bundle):
        try:
            del bundle.data['raw_password']
        except KeyError:
            pass
        return bundle

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/login%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name='api_login'),
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
                client_id, client_secret = retrieve_oauth_client(user)
                return self.create_response(request, {
                    'success': True,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'type': user.profile.type,
                    'user_url': '/api/v1/user/%d/' % (user.id,),
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


class UserCreateResource(ModelResource):
    user = fields.ForeignKey('api.api.UserResource', 'user', full=True)

    class Meta:
        allowed_methods = ['post']
        always_return_data = True
        authentication = Authentication()
        authorization = Authorization()
        queryset = UserProfile.objects.all()
        resource_name = 'create_user'
        always_return_data = True

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()

    def hydrate(self, bundle):
        REQUIRED_USER_PROFILE_FIELDS = ('name', 'user', 'contact_number',)
        for field in REQUIRED_USER_PROFILE_FIELDS:
            if bundle.data.get(field) == "":
                raise CustomBadRequest(
                    code='missing_key',
                    message='{missing_key} field is required.'
                            .format(missing_key=field).capitalize())

        REQUIRED_USER_FIELDS = ('username', 'email', 'raw_password')
        for field in REQUIRED_USER_FIELDS:
            if bundle.data['user'].get(field) == "":
                raise CustomBadRequest(
                    code='missing_key',
                    message='{missing_key} field is required.'
                            .format(missing_key=field).capitalize())
        return bundle

    def obj_create(self, bundle, **kwargs):
        try:
            email = bundle.data['user']['email']
            username = bundle.data['user']['username']
            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    code='duplicate_exception',
                    message='That email is already used.')
            if User.objects.filter(username=username):
                raise CustomBadRequest(
                    code='duplicate_exception',
                    message='That username is already used.')
        except KeyError as missing_key:
            raise CustomBadRequest(
                code='missing_key',
                message='{missing_key} field is required.'
                        .format(missing_key=missing_key).capitalize())
        except User.DoesNotExist:
            pass

        self._meta.resource_name = UserProfileResource._meta.resource_name
        return super(UserCreateResource, self).obj_create(bundle, **kwargs)


class UserProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        authentication = OAuth20Authentication()
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'patch', ]
        detail_allowed_methods = ['get', 'patch', 'put']
        queryset = UserProfile.objects.all()
        resource_name = 'user_profile'

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user).select_related()

    def get_list(self, request, **kwargs):
        kwargs['pk'] = request.user.profile.pk
        return super(UserProfileResource, self).get_detail(request, **kwargs)


class DeviceTokenResource(ModelResource):
    class Meta:
        queryset = DeviceToken.objects.all()
        resource_name = 'devicetoken'
        allowed_methods = ['get', 'post',]
        authentication = OAuth20Authentication()
        authorization = Authorization()
        validation = FormValidation(form_class=DeviceTokenForm)


class NotificationResource(ModelResource):
    class Meta:
        queryset = Notification.objects.all()
        resource_name = 'notification'
        allowed_methods = ['get', 'post',]
        authentication = OAuth20Authentication()
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
        }


class BookResource(ModelResource):
    class Meta:
        queryset = Book.objects.all()
        resource_name = 'book'
        allowed_methods = ['get', 'post',]
        authentication = OAuth20Authentication()
        authorization = Authorization()
        filtering = {
            'dentist': ALL_WITH_RELATIONS,
        }


class PhotoResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Photo.objects.all()
        resource_name = 'photo'
        allowed_methods = ['get', 'post',]
        authentication = OAuth20Authentication()
        authorization = Authorization()
        filtering = {
            'dentist': ALL_WITH_RELATIONS,
        }


class DentistProfileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = DentistProfile.objects.all()
        resource_name = 'dentist_profile'
        allowed_methods = ['get', 'post', 'patch', 'put',]
        authentication = OAuth20Authentication()
        authorization = Authorization()
        filtering = {
            'dentist': ALL_WITH_RELATIONS,
        }

        @property
        def validation(self):
            return ModelFormValidation(form_class=DentistProfileForm, \
                                            resource=DentistProfileResource)


class AppointmentResource(ModelResource):
    dentist = fields.ForeignKey(UserResource, 'dentist')

    class Meta:
        queryset = Appointment.objects.all()
        resource_name = 'appointment'
        allowed_methods = ['get', 'post',]
        authentication = OAuth20Authentication()
        authorization = Authorization()
        filtering = {
            'patient': ALL_WITH_RELATIONS,
            'dentist': ALL_WITH_RELATIONS,
        }

        @property
        def validation(self):
            return ModelFormValidation(form_class=AppointmentForm, \
                                            resource=AppointmentResource)


class EmergencyScheduleResource(ModelResource):
    dentist = fields.ForeignKey(UserResource, 'dentist')

    class Meta:
        queryset = EmergencySchedule.objects.all()
        resource_name = 'emergencyschedule'
        allowed_methods = ['get', 'post', 'patch',]
        authentication = OAuth20Authentication()
        authorization = Authorization()
        filtering = {
            'dentist': ALL_WITH_RELATIONS,
            'is_booked': ['exact'],
        }

        @property
        def validation(self):
            return ModelFormValidation(form_class=EmergencyScheduleForm, \
                                            resource=EmergencyScheduleResource)

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/weekly%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('weekly'), name='emergencyschedule_weekly'),
        ]

    def weekly(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        is_booked = request.GET.get('is_booked')
        is_booked = None if is_booked is None else is_booked == 'True'

        week_schedule = OrderedDict()
        current_date = datetime.utcnow().date()

        for daygap in range(6):
            date = current_date + timedelta(days=daygap)
            schedules = EmergencySchedule.objects.filter(date=date)

            if is_booked is not None:
                schedules = schedules.filter(is_booked=is_booked)

            if schedules.count():
                schedules_list = [json.loads(json.dumps(schedule, cls=DjangoJSONEncoder)) for schedule in schedules.values()]

                week_schedule.update({date.strftime('%B %d, %Y'): schedules_list})

        return self.create_response(request, {'objects': week_schedule })
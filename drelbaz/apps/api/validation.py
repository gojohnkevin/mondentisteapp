from django.forms.models import ModelChoiceField

from tastypie.validation import FormValidation
from tastypie.resources import ModelResource


class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    resource = ModelResource

    def __init__(self, **kwargs):
        if not 'resource' in kwargs:
            raise ImproperlyConfigured("You must provide a 'resource' to 'ModelFormValidation' classes.")

        self.resource = kwargs.pop('resource')

        super(ModelFormValidation, self).__init__(**kwargs)

    def form_args(self, bundle):
        rsc = self.resource()

        kwargs = super(ModelFormValidation, self).form_args(bundle)

        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if (field in kwargs['data']) and (field in rsc.fields) and (kwargs['data'][field] != None):
                toRsc = rsc.fields[field].to()
                kwargs['data'][field] = kwargs['data'][field].replace(toRsc.get_resource_uri(), "").replace("/", "")

        return kwargs

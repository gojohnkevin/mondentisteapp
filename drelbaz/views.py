from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.utils import simplejson as json

from drelbaz.libs.mixins import SiteWideMixin

from misc.models import DentalClinic


class HomeView(SiteWideMixin, View):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        return super(HomeView, self).get_context_data(**{
                    'clinics' : json.dumps(DentalClinic.get_all_json()),
                    })


def send_inquiry(request):
    pass

home = HomeView.as_view()

from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from drelbaz.libs.mixins import SiteWideMixin


class HomeView(SiteWideMixin, View):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        return super(HomeView, self).get_context_data(*args, **kwargs)

home = HomeView.as_view()

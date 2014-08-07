from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from accounts.forms import LoginForm
from drelbaz.libs.mixins import SiteWideMixin


class LoginView(SiteWideMixin, View):
    template_name = 'accounts/login.html'

    def get_context_data(self, *args, **kwargs):
        return super(LoginView, self).get_context_data(**{
            'login_form': kwargs.get('login_form') or LoginForm()
        })

    def dispatch(self, request, *args, **kwargs):
        destination = request.GET.get('next', reverse('home'))
        if request.user.is_authenticated():
            return HttpResponseRedirect(destination)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        destination = request.POST.get('next', reverse('home'))
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            auth.login(request, user)
            return HttpResponseRedirect(destination)
        else:
            response = self.render_to_response(self.get_context_data(**{
                            'login_form': form
                        }), status=401)
            response['auth-response'] = 'authError'
            return response

login = LoginView.as_view()

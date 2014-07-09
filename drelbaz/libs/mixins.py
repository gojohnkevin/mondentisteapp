from django.views.generic.base import TemplateResponseMixin


class SiteWideMixin(TemplateResponseMixin):
    """
    A mixin that will have context data or other functions to
    be used sitewide.
    """

    def __init__(self):
        user = None

    def get_context_data(self, *args, **context):
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(*args, **kwargs))

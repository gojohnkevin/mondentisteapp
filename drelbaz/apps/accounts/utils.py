from django.contrib.auth.models import User

from provider.oauth2.models import Client


def create_client(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(
                        user=instance,
                        name=instance.username,
                        url='http://mondentisteapp.com',
                        redirect_uri='http://mondentisteapp.com',
                        client_type=0)
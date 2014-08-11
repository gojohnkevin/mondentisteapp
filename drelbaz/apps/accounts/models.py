import json
import os
import time

from cStringIO import StringIO

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from apns import APNs, Payload
from PIL import Image
from tastypie.utils.timezone import now

from drelbaz.libs.apns import send_push


def get_photo_upload_path(instance, filename):
    return os.path.join('photos', 'user_%d' % instance.user.id, filename)
def get_thumbnail_upload_path(instance, filename):
    return os.path.join('thumbnails', 'user_%d' % instance.user.id, filename)

optional = {
    'null' : True,
    'blank': True,
}

class DeviceToken(models.Model):
    token = models.CharField(max_length=150, unique=True)

    def __unicode__(self):
        return u'%s' % (self.token,)


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=get_photo_upload_path)
    image_height = models.IntegerField(**optional)
    image_width = models.IntegerField(**optional)
    thumbnail = models.ImageField(upload_to=get_thumbnail_upload_path, **optional)
    thumbnail_height = models.IntegerField(**optional)
    thumbnail_width = models.IntegerField(**optional)

    user = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=now)

    def __unicode__(self):
        return u'%s' % (self.title,)

    def save(self, force_update=False, force_insert=False, thumb_size=(180,300)):

        image = Image.open(self.image)

        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        # save the original size
        self.image_width, self.image_height = image.size

        image.thumbnail(thumb_size, Image.ANTIALIAS)

        # save the thumbnail to memory
        temp_handle = StringIO()
        image.save(temp_handle, 'png')
        temp_handle.seek(0) # rewind the file

        # save to the thumbnail field
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                 temp_handle.read(),
                                 content_type='image/png')
        self.thumbnail.save(suf.name+'.png', suf, save=False)
        self.thumbnail_width, self.thumbnail_height = image.size

        # save the image object
        super(Photo, self).save(force_update, force_insert)


class DentistDetail(models.Model):
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)

    facebook = models.CharField(max_length=150, null=True, blank=True)
    twitter = models.CharField(max_length=150, null=True, blank=True)

    map = models.URLField(null=True, blank=True)

    device_token = models.CharField(max_length=150, **optional)

    user = models.OneToOneField(User)
    pub_date = models.DateTimeField(default=now, **optional)

    def __unicode__(self):
        return u'%s' % (self.user,)


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('declined', 'declined'),
        ('accepted', 'accepted'),
        ('canceled', 'canceled'),
    )
    #user fields
    name = models.CharField(max_length=100)
    email = models.EmailField(**optional)
    contact_number = models.CharField(max_length=25)
    device_token = models.CharField(max_length=150)
    message = models.TextField()

    #dentist fields
    dentist = models.ForeignKey(User)
    schedule = models.DateTimeField(**optional)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __unicode__(self):
        return u'%s' % (self.name,)

    def save(self, *args, **kwargs):
        super(Appointment, self).save(*args, **kwargs)
        if self.dentist.dentistdetail.device_token:
            apns = APNs(use_sandbox=True, cert_file=settings.APN_CERT_LOCATION, key_file=settings.APN_KEY_LOCATION)

            # Send a notification
            token_hex = self.dentist.dentistdetail.device_token
            payload = Payload(alert="Hello World!", sound="default", badge=1)
            apns.gateway_server.send_notification(token_hex, payload)
            #send_push(self.dentist.dentistdetail.device_token, json.dumps(PAYLOAD))


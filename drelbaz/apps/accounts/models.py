# -*- coding: utf-8 -*-

import json
import os
import time

from cStringIO import StringIO

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from apns import APNs, Frame, Payload
from PIL import Image
from tastypie.utils.timezone import now

from drelbaz.libs.apns import send_push


def get_photo_upload_path(instance, filename):
    return os.path.join('photos', 'user_%d' % instance.user.id, filename)
def get_thumbnail_upload_path(instance, filename):
    return os.path.join('thumbnails', 'user_%d' % instance.user.id, filename)
def get_book_photo_upload_path(instance, filename):
    return os.path.join('books', 'user_%d' % instance.dentist.id, filename)
def get_note_photo_upload_path(instance, filename):
    return os.path.join('notes', '%s' % instance.device_token, filename)

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


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(**optional)
    image = models.ImageField(upload_to=get_book_photo_upload_path, **optional)
    url = models.URLField()

    dentist = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.title,)


class DentistDetail(models.Model):
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()

    facebook = models.CharField(max_length=150, **optional)
    twitter = models.CharField(max_length=150, **optional)

    map = models.URLField(**optional)

    about = models.TextField(**optional)
    patient_education = models.TextField(**optional)

    device_token = models.CharField(max_length=150, **optional)

    user = models.OneToOneField(User)
    pub_date = models.DateTimeField(default=now, **optional)

    def __unicode__(self):
        return u'%s' % (self.user,)


class Notification(models.Model):
    device_token = models.CharField(max_length=150, **optional)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % (self.device_token,)


class Note(models.Model):
    image = models.ImageField(upload_to=get_note_photo_upload_path)
    comment = models.TextField(**optional)
    device_token = models.CharField(max_length=150, **optional)

    def __unicode__(self):
        return u'%s' % (self.device_token,)


class EmergencySchedule(models.Model):
    dentist = models.ForeignKey(User)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('dentist', 'date', 'time',)

    def __unicode__(self):
        return u'%s' % (self.dentist,)

    def save(self, *args, **kwargs):
        super(EmergencySchedule, self).save(*args, **kwargs)
        if not self.is_booked:
            if self.dentist.dentistdetail.device_token:
                apns = APNs(use_sandbox=False, cert_file=settings.APN_CERT_LOCATION, key_file=settings.APN_KEY_LOCATION)

                # Send a notification
                token_hex = self.dentist.dentistdetail.device_token
                alert_message = 'New appointment schedule for Dr. Elbaz is available  at %s.' % (self.date.strftime('%b %d,%Y'), (self.time.strftime('%I:%M %p')))
                payload = Payload(alert=alert_message, sound="default", badge=1)

                frame = Frame()
                identifier = 1
                expiry = time.time()+3600
                priority = 10
                for device_token in DeviceToken.objects.all():
                    frame.add_item(device_token.token, payload, identifier, expiry, priority)
                    notification = Notification(message=alert_message, device_token=device_token.token)
                    notification.save()
                apns.gateway_server.send_notification_multiple(frame)


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('accepted', 'Accepted'),
        ('canceled', 'Canceled'),
    )

    PURPOSE_CHOICES = (
        (u'Consultation dentaire', 'Consultation dentaire'),
        (u'Bilan complet', 'Bilan complet'),
        (u'Détartrage', 'Détartrage'),
        (u'Urgence dentaire', 'Urgence dentaire'),
        (u'Blanchiment', 'Blanchiment'),
        (u'Devis prothèse', 'Devis prothèse'),
        (u'Devis implants', 'Devis implants'),
        (u'Autres', 'Autres'),
    )

    #user fields
    name = models.CharField(max_length=100)
    email = models.EmailField(**optional)
    contact_number = models.CharField(max_length=25)
    date = models.DateField()
    time = models.TimeField()
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    comment = models.TextField(**optional)
    created = models.DateTimeField(auto_now_add=True)
    device_token = models.CharField(max_length=150)

    #dentist fields
    dentist = models.ForeignKey(User)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % (self.name,)

    def save(self, *args, **kwargs):
        super(Appointment, self).save(*args, **kwargs)
        if self.status == 'pending':
            if self.dentist.dentistdetail.device_token:
                apns = APNs(use_sandbox=False, cert_file=settings.APN_CERT_LOCATION, key_file=settings.APN_KEY_LOCATION)

                # Send a notification
                token_hex = self.dentist.dentistdetail.device_token
                alert_message = self.name + ' requested for an appointment on %s - %s.'  % (self.date.strftime('%b %d,%Y'), (self.time.strftime('%I:%M %p')))
                notification = Notification(message=alert_message, device_token=token_hex)
                notification.save()
                payload = Payload(alert=alert_message, sound="default", badge=1)
                apns.gateway_server.send_notification(token_hex, payload)
        else:
            if self.device_token:
                apns = APNs(use_sandbox=False, cert_file=settings.APN_CERT_LOCATION, key_file=settings.APN_KEY_LOCATION)

                # Send a notification
                token_hex = self.device_token
                if self.status == 'declined':
                    alert_message = 'Your appointment request has been declined. Please contact us for further details.'
                elif self.status == 'accepted':
                    alert_message = 'Your appointment request has been accepted. Please visit us on %s - %s.' % (self.date.strftime('%b %d,%Y'), (self.time.strftime('%I:%M %p')))
                payload = Payload(alert=alert_message, sound="default", badge=1)
                notification = Notification(message=alert_message, device_token=token_hex)
                notification.save()
                apns.gateway_server.send_notification(token_hex, payload)


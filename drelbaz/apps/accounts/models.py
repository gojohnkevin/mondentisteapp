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
    return os.path.join('notes', '%s' % instance.user.id, filename)

optional = {
    'null' : True,
    'blank': True,
}

class DeviceToken(models.Model):
    token = models.CharField(max_length=150, **optional)

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

    dentist = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add=True)

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


class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    user = models.OneToOneField(User, related_name='profile')
    dentist = models.ForeignKey(User, related_name='patient')
    device_token = models.ManyToManyField(DeviceToken, **optional)

    def __unicode__(self):
        return u'%s' % (self.name,)


class DentistProfile(models.Model):
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()

    facebook = models.CharField(max_length=150, **optional)
    twitter = models.CharField(max_length=150, **optional)

    map = models.URLField(**optional)

    about = models.TextField(**optional)
    patient_education = models.TextField(**optional)

    dentist = models.OneToOneField(User)
    device_token = models.ManyToManyField(DeviceToken, **optional)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.dentist.get_full_name(),)


class Notification(models.Model):
    user = models.ForeignKey(User)
    message = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s - %s' % (self.user, self.message,)


class Note(models.Model):
    image = models.ImageField(upload_to=get_note_photo_upload_path)
    comment = models.TextField(**optional)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % (self.user,)


class EmergencySchedule(models.Model):
    dentist = models.ForeignKey(User)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date', 'time',)
        unique_together = ('dentist', 'date', 'time',)

    def __unicode__(self):
        return u'%s - %s %s' % (self.dentist.get_full_name(), unicode(self.date), unicode(self.time))

    def save(self, *args, **kwargs):
        super(EmergencySchedule, self).save(*args, **kwargs)
        if not self.is_booked:
            if self.dentist.dentistprofile.device_token:
                apns = APNs(use_sandbox=False, cert_file=settings.APN_CERT_LOCATION, key_file=settings.APN_KEY_LOCATION)

                # Send a notification
                token_hex = self.dentist.dentistprofile.device_token.all()[0].token
                alert_message = 'New appointment schedule for Dr. Elbaz is available  at %s - %s.' % (self.date.strftime('%b %d,%Y'), (self.time.strftime('%I:%M %p')))
                payload = Payload(alert=alert_message, sound="default", badge=1)

                frame = Frame()
                identifier = 1
                expiry = time.time()+3600
                priority = 10
                for patient in UserProfile.objects.filter(dentist=self.dentist):
                    frame.add_item(patient.device_token.all()[0].token, payload, identifier, expiry, priority)
                    notification = Notification(message=alert_message, user=patient.user)
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
    date = models.DateField()
    time = models.TimeField()
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    comment = models.TextField(**optional)
    created = models.DateTimeField(auto_now_add=True)

    dentist = models.ForeignKey(User, related_name='dentist_apts')
    patient = models.ForeignKey(User, related_name='patient_apts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % (self.patient.profile.name,)

    def save(self, *args, **kwargs):
        super(Appointment, self).save(*args, **kwargs)
        if self.status == 'pending':
            if self.dentist.dentistprofile.device_token:
                apns = APNs(use_sandbox=False, cert_file=settings.APN_CERT_LOCATION, key_file=settings.APN_KEY_LOCATION)

                # Send a notification
                token_hex = self.dentist.dentistprofile.device_token.all()[0].token
                alert_message = self.patient.profile.name + ' requested for an appointment on %s - %s.'  % (self.date.strftime('%b %d,%Y'), (self.time.strftime('%I:%M %p')))
                notification = Notification(message=alert_message, user=self.dentist)
                notification.save()
                payload = Payload(alert=alert_message, sound="default", badge=1)
                apns.gateway_server.send_notification(token_hex, payload)
        else:
            if self.status != 'pending':
                apns = APNs(use_sandbox=False, cert_file=settings.APN_CERT_LOCATION, key_file=settings.APN_KEY_LOCATION)

                # Send a notification
                token_hex = self.patient.profile.device_token.all()[0].token
                if self.status == 'declined':
                    alert_message = 'Your appointment request has been declined. Please contact us for further details.'
                elif self.status == 'accepted':
                    alert_message = 'Your appointment request has been accepted. Please visit us on %s - %s.' % (self.date.strftime('%b %d,%Y'), (self.time.strftime('%I:%M %p')))
                payload = Payload(alert=alert_message, sound="default", badge=1)
                notification = Notification(message=alert_message, user=self.patient)
                notification.save()
                apns.gateway_server.send_notification(token_hex, payload)


#===========================================================================
# SIGNALS
#===========================================================================
def signals_import():
    """ A note on signals.

    The signals need to be imported early on so that they get registered
    by the application. Putting the signals here makes sure of this since
    the models package gets imported on the application startup.
    """
    from accounts.utils import create_client

    models.signals.post_save.connect(create_client, sender=User)

signals_import()
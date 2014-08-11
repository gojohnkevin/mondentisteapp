import os

from cStringIO import StringIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from PIL import Image
from tastypie.utils.timezone import now


def get_photo_upload_path(instance, filename):
    return os.path.join('photos', 'user_%d' % instance.user.id, filename)
def get_thumbnail_upload_path(instance, filename):
    return os.path.join('thumbnails', 'user_%d' % instance.user.id, filename)

optional = {
    'null' : True,
    'blank': True,
}

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

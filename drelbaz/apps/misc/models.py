from django.db import models

# Create your models here.
class DentalClinic(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False)
    dentist = models.CharField(max_length=100, unique=True, blank=False)
    longitude = models.CharField(max_length=150, help_text="Latitude", null=True, blank=True)
    latitude = models.CharField(max_length=150, help_text="Latitude", null=True, blank=True)


    @classmethod
    def get_all_json(cls):
        """
        returns a serializable dict object; same as the serialize method
        """

        clinics = cls.objects.all()
        json_array = []

        for clinic in clinics:
            json_form = {'id': clinic.id,
                         'name': clinic.name,
                         'dentist': clinic.dentist,
                         'longitude': clinic.longitude,
                         'latitude': clinic.latitude, }

            json_array.append(json_form)

        return json_array


class Blog(models.Model):
    title = models.CharField(max_length=150, unique=True)
    content = models.TextField(max_length=10000)
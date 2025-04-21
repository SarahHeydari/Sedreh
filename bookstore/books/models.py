from django.contrib.gis.db import models
from django.conf import settings
from django.contrib.gis.geos import Point
# Create your models here.


class Book(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    available = models.BooleanField(default=True)
#   bookshop_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class County(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.PolygonField(geography=True)

    def __str__(self):
        return self.name

class Bookshop(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField(geography=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

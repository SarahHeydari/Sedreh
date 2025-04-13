from django.contrib.gis.db import models
from django.conf import settings

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# class county()
#     name
#     coordinates

# class bookstores()
#     name
    # location

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

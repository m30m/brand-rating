from django.db import models


class Brand(models.Model):
    name = models.TextField()
    image = models.ImageField()


class BrandRating(models.Model):
    brand = models.ForeignKey(Brand)
    rating = models.SmallIntegerField()
    ip = models.GenericIPAddressField()

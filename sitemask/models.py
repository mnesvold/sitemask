from django.db import models


class Mask(models.Model):
    title = models.TextField(blank=True)
    subtitle = models.TextField(blank=True)
    image = models.ImageField()
    effective = models.DateTimeField()
    expiration = models.DateTimeField()

    class Meta:
        unique_together = (('effective', 'expiration'),)

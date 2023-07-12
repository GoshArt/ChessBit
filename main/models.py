from django.db import models


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=255)
    succ = models.CharField(max_length=255)


class Gosha(models.Model):
    name = models.TextField(max_length=255)
    iq = models.CharField(max_length=2)

    def __str__(self):
        return self.name + " " + self.iq

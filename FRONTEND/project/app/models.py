from django.db import models

# Create your models here.
class Univesity(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    contact = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return self.name
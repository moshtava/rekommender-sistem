from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
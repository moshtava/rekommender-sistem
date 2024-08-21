from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    
class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    amount = models.FloatField()
    date = models.DateTimeField()    
    
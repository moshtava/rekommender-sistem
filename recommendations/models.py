from django.db import models

class Transaction(models.Model):
   user_id = models.IntegerField()
   crypto_id = models.IntegerField()
   transaction_type = models.CharField(max_length=4)
   transaction_amount = models.FloatField()
   transaction_date = models.DateTimeField()
   user_age = models.IntegerField()
   user_location = models.CharField(max_length=10)
   crypto_price = models.FloatField()
   market_trend = models.CharField(max_length=7)
   user_balance = models.FloatField()
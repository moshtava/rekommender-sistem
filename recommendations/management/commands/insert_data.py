import datetime
import os
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.calibration import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from recommendations.models import Transaction
import xgboost as xgb

class Command(BaseCommand):
   help = 'Insert 10,000 transactions into the database'
   
   def handle(self, *args, **kwargs):
      num_samples = 10000
      num_users = 100
      data = {
      'user_id': np.random.randint(1, num_users + 1, num_samples),
      'crypto_id': np.random.randint(1, 21, num_samples),  # i'm assuming 20 different currencies
      'transaction_type': np.random.choice(['buy', 'sell'], num_samples),
      'transaction_amount': np.round(np.random.uniform(0.1, 5.0, num_samples), 2),
      'transaction_date': [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(num_samples)],
      'user_age': np.random.randint(18, 60, num_samples),
      'user_location': np.random.choice(['USA', 'Canada', 'Iran', 'Germany', 'Japan'], num_samples),
      'crypto_price': np.round(np.random.uniform(1000, 50000, num_samples), 2),
      'market_trend': np.random.choice(['bullish', 'bearish'], num_samples),
      'user_balance': np.round(np.random.uniform(1000, 100000, num_samples), 2)
      }
      df = pd.DataFrame(data)
      transactions = [Transaction(**row) for row in df.to_dict(orient='records')]
      Transaction.objects.bulk_create(transactions)
      self.stdout.write(self.style.SUCCESS('Successfully inserted 10,000 transactions'))
      
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
      self.train_xgbst()
      
   def train_xgbst(self):
      transactions = Transaction.objects.all().values()
      df = pd.DataFrame(transactions)
      label_encoders = {}
      for column in ['transaction_type', 'user_location', 'market_trend']:
         le = LabelEncoder()
         df[column] = le.fit_transform(df[column])
         label_encoders[column] = le
      X = df.drop(['transaction_amount', 'transaction_date'], axis=1)
      y = df['transaction_amount']
      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
      dtrain = xgb.DMatrix(X_train, label=y_train)
      dtest = xgb.DMatrix(X_test, label=y_test)
      params = {
      'objective': 'reg:squarederror',
      'max_depth': 6,
      'eta': 0.3,
      'eval_metric': 'rmse'
      }
      bst = xgb.train(params, dtrain, num_boost_round=100)
      y_pred = bst.predict(dtest)
      rmse = mean_squared_error(y_test, y_pred, squared=False)
      self.stdout.write(self.style.SUCCESS(f"RMSE: {rmse}"))
      project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      model_path = os.path.join(project_dir, 'xgboost_model.json')
      bst.save_model(model_path)
      self.stdout.write(self.style.SUCCESS(f"Model saved to {model_path}"))

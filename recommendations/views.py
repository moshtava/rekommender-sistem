import datetime
import os
import numpy as np
from rest_framework import generics
from sklearn.calibration import LabelEncoder
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response
import xgboost as xgb
import pandas as pd

class TransactionRetrieve(generics.RetrieveAPIView):
   queryset = Transaction.objects.all()
   serializer_class = TransactionSerializer
   
   def get(self, request, user_id):
      transactions = Transaction.objects.filter(user_id=user_id)
      if not transactions.exists():
         return Response({"error": "User not found"}, status=404)      
      df = pd.DataFrame(list(transactions.values()))
      label_encoders = {}
      for column in ['transaction_type', 'user_location', 'market_trend']:
         le = LabelEncoder()
         df[column] = le.fit_transform(df[column])
         label_encoders[column] = le
      model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'xgboost_model.json')
      bst = xgb.Booster()
      bst.load_model(model_path)
      user_data = df.drop(['transaction_amount', 'transaction_date'], axis=1)
      duser = xgb.DMatrix(user_data)
      predictions = bst.predict(duser)
      df['predicted_amount'] = predictions
      recommendations = df.sort_values(by='predicted_amount', ascending=False).head(5)
      return Response(recommendations[['crypto_id', 'predicted_amount']].to_dict(orient='records'))

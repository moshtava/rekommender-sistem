from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import xgboost as xgb
import pandas as pd

class TransactionListCreate(generics.ListCreateAPIView):
   queryset = Transaction.objects.all()
   serializer_class = TransactionSerializer
   
   @api_view(['GET'])
   def recommend_cryptos(request, user_id):
      transactions = Transaction.objects.filter(user_id=user_id)
      if not transactions.exists():
         return Response({"error": "User not found"}, status=404)
      
      df = pd.DataFrame(list(transactions.values()))
      bst = xgb.Booster()
      bst.load_model('xgboost_model.json')
      
      user_data = df.drop(['transaction_amount', 'transaction_date'], axis=1)
      duser = xgb.DMatrix(user_data)
      predictions = bst.predict(duser)
      df['predicted_amount'] = predictions
      recommendations = df.sort_values(by='predicted_amount', ascending=False).head(5)
      
      return Response(recommendations[['crypto_id', 'predicted_amount']].to_dict(orient='records'))

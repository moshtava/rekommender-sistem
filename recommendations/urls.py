from django.urls import path
from .views import TransactionListCreate, recommend_cryptos

urlpatterns = [
path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
path('recommend/<int:user_id>/', recommend_cryptos, name='recommend-cryptos'),
]
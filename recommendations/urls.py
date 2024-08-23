from django.urls import path
from .views import TransactionList, TransactionRetrieve

urlpatterns = [
    
path('transactions/', TransactionList.as_view(), name='transaction-list-create'),
path('recommend/<int:user_id>/', TransactionRetrieve.as_view(), name='recommend-cryptos'),
]
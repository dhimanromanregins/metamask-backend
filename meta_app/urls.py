# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('generate-ethereum-account/', GenerateEthereumAccount.as_view(), name='generate-ethereum-account'),
    path('ethereum-balance/<str:address>/', EthereumBalance.as_view(), name='ethereum-balance'),
    path('ethereum-transaction-history/<str:address>/', EthereumTransactionHistory.as_view(), name='ethereum-transaction-history'),
    path('token_info/<str:address>/', EthereumTokenInfo.as_view(), name='token-info'),
    path('eth_price/', EthPriceView.as_view(), name='eth_price'),
]

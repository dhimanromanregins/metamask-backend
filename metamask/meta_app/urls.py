# urls.py
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('generate-ethereum-account/', GenerateNetworkAccount.as_view(), name='generate-coin-account'),
    path('ethereum-balance/<str:address>/<str:symbol>', CoinBalance.as_view(), name='coin-balance'),
    path('coin-transaction-history/<str:address>/', CoinTransactionHistory.as_view(), name='coin-transaction-history'),
    path('token_info/<str:address>/', CoinTokenInfo.as_view(), name='token-info'),
    path('coin_price/', CoinPriceView.as_view(), name='coin_price'),
    path('send_crypto/', SendCoinView.as_view(), name='send_coin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


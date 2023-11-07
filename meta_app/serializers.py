# serializers.py
from rest_framework import serializers
from .models import EthereumAccount , TokenContract

class EthereumAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EthereumAccount
        fields = ('user', 'address', 'private_key')


class TokenContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenContract
        fields = ['user','address']


class TokenInfoSerializer(serializers.Serializer):
    token_contract_address = serializers.CharField()
    balance = serializers.IntegerField()
    name = serializers.CharField()
    symbol = serializers.CharField()


class EthPriceSerializer(serializers.Serializer):
    ethereum_inr = serializers.FloatField()

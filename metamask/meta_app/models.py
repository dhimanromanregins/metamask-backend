from django.db import models
from Authentication.models import CustomUser

# Create your models here.


class ChainDetails(models.Model):
    chain_name = models.CharField(max_length=255, unique=True)
    chain = models.CharField(max_length=255, unique=True)
    chain_rpc = models.CharField(max_length=1000, unique=True)
    chain_symbol = models.CharField(max_length=100, unique=True)
    chain_logo = models.ImageField()
    def __str__(self):
        return self.chain_name

class EthereumAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    private_key = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class TokenContract(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return self.user.username

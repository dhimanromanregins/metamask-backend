from django.db import models
from Authentication.models import CustomUser

# Create your models here.
class EthereumAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)  # Ethereum address is 42 characters long
    private_key = models.CharField(max_length=100)


class TokenContract(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=42, unique=True)

    def __str__(self):
        return self.user.username
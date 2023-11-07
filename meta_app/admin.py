# admin.py
from django.contrib import admin
from .models import EthereumAccount

@admin.register(EthereumAccount)
class EthereumAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'private_key')

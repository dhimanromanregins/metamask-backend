from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from faker import Faker

fake = Faker()

class CustomUser(AbstractUser):
    custom_id = models.CharField(max_length=255, unique=True, editable=False)
    secret_phrase_1 = models.CharField(max_length=200, blank=True)
    secret_phrase_2 = models.CharField(max_length=200, blank=True)
    secret_phrase_3 = models.CharField(max_length=200, blank=True)
    secret_phrase_4 = models.CharField(max_length=200, blank=True)
    secret_phrase_5 = models.CharField(max_length=200, blank=True)
    secret_phrase_6 = models.CharField(max_length=200, blank=True)
    secret_phrase_7 = models.CharField(max_length=200, blank=True)
    secret_phrase_8 = models.CharField(max_length=200, blank=True)
    secret_phrase_9 = models.CharField(max_length=200, blank=True)
    secret_phrase_10 = models.CharField(max_length=200, blank=True)
    secret_phrase_11 = models.CharField(max_length=200, blank=True)
    secret_phrase_12 = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            # Generate a random 7-digit number and prepend 'ID-'
            self.custom_id = f'ID-{get_random_string(length=7, allowed_chars="1234567890")}'

        super(CustomUser, self).save(*args, **kwargs)
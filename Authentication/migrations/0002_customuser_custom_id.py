# Generated by Django 4.2.6 on 2023-10-30 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='custom_id',
            field=models.CharField(default=1, editable=False, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]

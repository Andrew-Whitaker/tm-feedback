# Generated by Django 3.0.7 on 2020-07-27 21:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0006_auto_20200721_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='membership_requests',
            field=models.ManyToManyField(related_name='pending_clubs', to=settings.AUTH_USER_MODEL),
        ),
    ]

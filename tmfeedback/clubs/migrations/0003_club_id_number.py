# Generated by Django 3.0.7 on 2020-06-30 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20200630_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='id_number',
            field=models.PositiveIntegerField(default=0, unique=True),
        ),
    ]

# Generated by Django 3.0.7 on 2020-07-21 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_club_id_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='id_number',
            new_name='tm_id',
        ),
        migrations.RemoveField(
            model_name='club',
            name='summary',
        ),
        migrations.AddField(
            model_name='club',
            name='description',
            field=models.TextField(default='', max_length=1500),
        ),
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
# Generated by Django 3.0.7 on 2020-07-09 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_remove_booking_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='type',
            field=models.CharField(default='', max_length=20),
        ),
    ]
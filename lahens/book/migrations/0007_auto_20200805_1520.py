# Generated by Django 3.0.7 on 2020-08-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathtk',
            name='last_spot',
            field=models.CharField(default='', max_length=100),
        ),
    ]

# Generated by Django 3.0.7 on 2020-08-08 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_auto_20200808_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingi',
            name='book_date',
            field=models.DateTimeField(),
        ),
    ]
# Generated by Django 3.0.7 on 2020-07-07 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=90)),
                ('seat_no', models.IntegerField(default=0)),
                ('bus_id', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=20)),
                ('book_date', models.DateField()),
                ('froml', models.CharField(max_length=200)),
                ('tol', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='BusI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_name', models.CharField(max_length=50)),
                ('seat_count', models.IntegerField(default=0)),
                ('dest_count', models.IntegerField(default=0)),
                ('path', models.CharField(max_length=2000)),
                ('timings', models.CharField(max_length=2000)),
                ('distance', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=200)),
                ('froml', models.CharField(max_length=200)),
                ('tol', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('desc', models.CharField(max_length=2000)),
            ],
        ),
    ]
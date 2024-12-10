# Generated by Django 5.1.3 on 2024-11-22 23:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=50)),
                ('duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='posters/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('cinema_hall', models.CharField(max_length=100)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tickets', models.PositiveIntegerField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.showtime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.user')),
            ],
        ),
    ]

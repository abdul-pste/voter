# Generated by Django 5.1.3 on 2024-12-04 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_remove_booking_tickets_remove_booking_total_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='showtime',
            name='cinema_hall',
            field=models.CharField(default='Unknown Location', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='showtime',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='showtime',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
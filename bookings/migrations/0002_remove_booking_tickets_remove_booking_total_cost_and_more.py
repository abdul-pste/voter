# Generated by Django 5.1.3 on 2024-12-04 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='tickets',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='total_cost',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='poster',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='cinema_hall',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='date',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='time',
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
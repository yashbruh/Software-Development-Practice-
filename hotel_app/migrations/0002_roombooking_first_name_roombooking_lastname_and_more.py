# Generated by Django 5.1.4 on 2024-12-16 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='roombooking',
            name='First_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='roombooking',
            name='Lastname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='roombooking',
            name='email_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
# Generated by Django 5.1.1 on 2024-10-11 11:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0072_remove_loading_labour_advance_payment_userprofile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loading_labour_advance_payment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='production_labour_advance_payment',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

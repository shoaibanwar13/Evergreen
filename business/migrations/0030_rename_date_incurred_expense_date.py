# Generated by Django 5.0.2 on 2024-07-04 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0029_expense'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='date_incurred',
            new_name='date',
        ),
    ]

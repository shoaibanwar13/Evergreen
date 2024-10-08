# Generated by Django 5.0.2 on 2024-08-05 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0053_expense_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='Paid_Amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='Remaining_Amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]

# Generated by Django 5.0.2 on 2024-08-05 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0057_alter_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='Bill_Proof',
            field=models.ImageField(blank=True, null=True, upload_to='Expenses Bill'),
        ),
    ]

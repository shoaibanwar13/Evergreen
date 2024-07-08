# Generated by Django 5.0.2 on 2024-07-07 06:49

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0032_manufacturing_manufacture_weight'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='userprofile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='Profit_OR_Lose',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='Manufacture_Weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='Weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Pending_Payments',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Recived_Payments',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Total_Expense',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Total_Purchase',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Total_Sale',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.CreateModel(
            name='PaymentOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Profit', 'Profit'), ('Travel', 'Travel'), ('Utilities', 'Utilities'), ('Marketing', 'Marketing'), ('Other', 'Other')], default='Other', max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('Bill_Proof', models.ImageField(upload_to='Expenses Bill')),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Transaction', to=settings.AUTH_USER_MODEL)),
                ('userprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.profile')),
            ],
        ),
    ]

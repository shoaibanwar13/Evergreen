# Generated by Django 5.0.2 on 2024-06-21 10:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetail',
            name='phone',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='DailyProduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Puroduction_Product_Name', models.CharField(max_length=200)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('Production_Place', models.CharField(max_length=200)),
                ('City', models.CharField(blank=True, max_length=200, null=True)),
                ('Production_Team_Name', models.CharField(max_length=300)),
                ('Total_Production_Item', models.IntegerField(default=0)),
                ('Production_and_Expense_Proof_Screenshot', models.ImageField(upload_to='Production_and_Expense_Proof_Screenshot')),
                ('Total_Expense_Amount', models.IntegerField(default=0)),
                ('Remarks_of_Expense', models.CharField(max_length=3000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Productions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Manufeaturing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Manufeaturing_Product_Name', models.CharField(max_length=200)),
                ('Supplier_Name', models.CharField(max_length=200)),
                ('Place_Of_Supply', models.CharField(max_length=200)),
                ('City', models.CharField(max_length=200)),
                ('Weight', models.CharField(max_length=200)),
                ('Total_Production_Items', models.IntegerField(default=0)),
                ('Total_Purchase_Price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('Manufeaturing_Expense', models.IntegerField(default=0)),
                ('Total_Sale_Amount', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('Profit', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('Lose', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
    ]

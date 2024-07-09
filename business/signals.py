from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F
adminEmail=CompanyDetail.objects.get()
mail=adminEmail.email
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Sale)
def send_sale_email(sender, instance, created, **kwargs):
    if created:
        send_email_to_admin(instance)
        send_email_to_customer(instance)
@receiver(post_save, sender=DailyProduction)
def send_production_email(sender, instance, created, **kwargs):
    if created:
        send_dailyProductionemail_to_admin(instance)
def send_email_to_admin(sale):
    subject = f'New Sale: {sale.Sale_Production_Name}'
    message = (
        f'A new sale has been made.\n\n'
        f'Details:\n'
         f'Vendor: {sale.user}\n'
        f'Seller: {sale.user.first_name}\n'
        f'Production Name: {sale.Sale_Production_Name}\n'
        f'Item/Balles: {sale.Items_Or_Balles}\n'
        f'Weight: {sale.Items_Or_Balles}\n'
        f'Unit: {sale.Weight_Unit}\n'
        f'Sale Price: {sale.Sale_Price}\n'
        f'Total Amount: {sale.Total_Amount}\n'  
        f'Discount: {sale.Discount}\n'
        f'GST: {sale.GST}\n'
        f'Final Amount: {sale.Final_Amount}\n'
        f'Paid Amount: {sale.Paid_Amount}\n'
        f'Payment Status: {sale.Payment_Status}\n'
        f'Remaining: {sale.Remaining}\n'
        f'Client: {sale.Client_Name}\n'
        f'Phone: {sale.Client_Phone_Number}\n'
        f'Address: {sale.Shiping_Address}, {sale.Shipping_City}, {sale.Shiping_State}\n'
        f'Driver: {sale.Driver_Name}\n'
        f'Vehicle: {sale.Vehicle_Number}\n'
        f'Vehicle: {sale.Driver_Contact}\n'
    )
    admin_email = mail
    send_mail(subject, message, settings.EMAIL_HOST_USER, [admin_email])

def send_email_to_customer(sale):
    subject = f'Order Conformation From Evergreen Corn Silage And Dairy Deals: {sale.Sale_Production_Name}'
    message = (
        f'Thank you for buying.You order have been received and deliver within in 5 business days.\n\n'
        f'Details:\n'
        f'Production Name: {sale.Sale_Production_Name}\n'
        f'Item/Balles: {sale.Items_Or_Balles}\n'
        f'Weight: {sale.Items_Or_Balles}\n'
        f'Unit: {sale.Weight_Unit}\n'
        f'Sale Price: {sale.Sale_Price}\n'
        f'Total Amount: {sale.Total_Amount}\n'  
        f'Discount: {sale.Discount}\n'
        f'GST: {sale.GST}\n'
        f'Final Amount: {sale.Final_Amount}\n'
        f'Paid Amount: {sale.Paid_Amount}\n'
        f'Payment Status: {sale.Payment_Status}\n'
        f'Remaining: {sale.Remaining}\n'
        f'Client: {sale.Client_Name}\n'
        f'Phone: {sale.Client_Phone_Number}\n'
        f'Address: {sale.Shiping_Address}, {sale.Shipping_City}, {sale.Shiping_State}\n'
        f'Driver: {sale.Driver_Name}\n'
        f'Vehicle: {sale.Vehicle_Number}\n'
        f'Vehicle: {sale.Driver_Contact}\n'
    )
    send_mail(subject, message,  settings.EMAIL_HOST_USER, [sale.Client_ID.Email])


def send_dailyProductionemail_to_admin(production):
    subject = f'New Production Entry: {production.Puroduction_Product_Name}'
    message = (
        f'A new production entry has been made.\n\n'
        f'Details:\n'
        f'Vendor: {production.user}\n'
        f'Product: {production.Puroduction_Product_Name}\n'
        f'Date: {production.date}\n'
        f'Place: {production.Production_Place}\n'
        f'City: {production.City}\n'
        f'Team: {production.Production_Team_Name}\n'
        f'Total Items: {production.Total_Production_Item}\n'
        f'Total Items: {production.Total_Production_Item}\n'
        f'Expense Amount: {production.Total_Expense_Amount}\n'
        f'Remarks: {production.Remarks_of_Expense}\n'
    )
    admin_email = mail
    send_mail(subject, message,  settings.EMAIL_HOST_USER, [admin_email])
@receiver(post_save, sender=Manufacturing)
def send_manufacturing_email(sender, instance, created, **kwargs):
    if created:
        send_Manufacturing_email_to_admin(instance)

def send_Manufacturing_email_to_admin(manufacturing):
    profile_expense=Profile.objects.filter(user=manufacturing.user).update(Total_Expense=F("Total_Expense")+manufacturing.Manufacturing_Expense
    ,Total_Purchase=F("Total_Purchase")+manufacturing.Total_Purchase_Price                                                                   

    )


    subject = f'New Manufacturing Entry: {manufacturing.Manufacturing_Product_Name}'
    message = (
        f'A new manufacturing entry has been made.\n\n'
        f'Details:\n'
        f'Vendor: {manufacturing.user}\n'
        f'Product: {manufacturing.Manufacturing_Product_Name}\n'
        f'Supplier: {manufacturing.Supplier_Name}\n'
        f'Place of Supply: {manufacturing.Place_Of_Supply}\n'
        f'City: {manufacturing.City}\n'
        f'Weight: {manufacturing.Manufacture_Weight}\n'
        f'Total Purchase Price: {manufacturing.Total_Purchase_Price}\n'
        f'Manufacturing Expense: {manufacturing.Manufacturing_Expense}\n'
    )
    admin_email = mail
    send_mail(subject, message, settings.EMAIL_HOST_USER , [admin_email])
@receiver(post_save, sender=Expense)
def send_email_to_admin_for_expense(sender, instance, created, **kwargs):
    if created:
        send_email_to_admin_for_expense(instance)

def send_email_to_admin_for_expense(expense):
    subject = f'New Expenses Entry: {expense.description}'
    message = (
        f'A new expense entry has been made.\n\n'
        f'Details:\n'
        f'Vendor: {expense.user}\n'
        f'Description: {expense.description}\n'
        f'Category: {expense.category}\n'
        f'Amount: {expense.amount}\n'
        f'Date: {expense.date}\n'
        f'Notes: {expense.notes}\n'
    )
    admin_email = mail
    send_mail(subject, message, settings.EMAIL_HOST_USER, [admin_email])
@receiver(post_save, sender=PaymentOut)
def send_paymentout_email(sender, instance, created, **kwargs):
    if created:
        send_email_to_admin_for_payment_out(instance)

def send_email_to_admin_for_payment_out(payment_out):
    subject = f'New Payment Out Entry: {payment_out.description}'
    message = (
        f'A new payment out entry has been made.\n\n'
        f'Details:\n'
        f'Name: {payment_out.name}\n'
        f'Description: {payment_out.description}\n'
        f'Category: {payment_out.category}\n'
        f'Amount: {payment_out.amount}\n'
        f'Date: {payment_out.date}\n'
        f'Notes: {payment_out.notes}\n'
        f'Vendor: {payment_out.user}\n'
    )
    admin_email = mail
    send_mail(subject, message, settings.EMAIL_HOST_USER, [admin_email])
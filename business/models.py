from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CompanyDetail(models.Model):
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="Company Logo")
    Head_Office=models.CharField(max_length=1000)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=30)
    Intro_Video=models.FileField(upload_to="videos", blank=True,max_length=2000)
    class Meta:
        verbose_name_plural="Company Detail"
    def __str__(self):
        return self.name
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(null=True)
    profilepic=models.ImageField(upload_to='profilepic/', null=True,blank=True)
    created=models.DateTimeField(auto_now=True)
    Total_Purchase=models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Total_Sale=models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Total_Expense=models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Profit_OR_Lose=models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Balance=models.DecimalField(max_digits=20, decimal_places=2,default=0)
    phone=models.CharField(max_length=200,null=True)
    
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    country=models.CharField(max_length=200,null=True)
    def __str__(self) :

        return  f"{self.user.username}"
class Manufacturing(models.Model):
    user=models.ForeignKey(User,related_name="Product",on_delete=models.CASCADE)
    userprofile = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Manufacturing_Product_Name=models.CharField(max_length=200,primary_key=True)
    Supplier_Name=models.CharField(max_length=200)
    Place_Of_Supply=models.CharField(max_length=200)
    City=models.CharField(max_length=200)
    Weight=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Manufacture_Weight=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Payment_Proof=models.ImageField(upload_to="Payment Proof/",null=True,blank=True)
    Total_Production_Items=models.IntegerField(default=0)
    Manufacture_Balles=models.IntegerField(default=0)
    Total_Purchase_Price=models.DecimalField( max_digits=20,decimal_places=2)
    Manufacturing_Expense=models.IntegerField(default=0)
    Total_Sale_Amount=models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True,default=0)
    Profit_OR_Lose=models.DecimalField( max_digits=20,decimal_places=2,null=True,blank=True,default=0)
    Complete_Production=models.BooleanField(default=False)
    Out_Of_Stock=models.BooleanField(default=False)
    KG = 'KG'
    MUN = 'MUN'
    QUANTITY="QUANTITY"
    OTHERS="OTHERS"
    STATUS_CHOICES = (
        ( KG, 'KG'),
        ( MUN, ' MUN'),
        ( QUANTITY,'QUANTITY'),
        (OTHERS,"OTHERS")
    )
    Unit = models.CharField(max_length=20, choices=STATUS_CHOICES, default=MUN)
    date=models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.Manufacturing_Product_Name}"




class DailyProduction(models.Model):
    user=models.ForeignKey(User,related_name="Productions",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Puroduction_Product_Name=models.CharField(max_length=200)
    date=models.DateField(default=timezone.now)
    Production_Place=models.CharField(max_length=200)
    City=models.CharField(max_length=200,blank=True,null=True)
    Production_Team_Name=models.CharField(max_length=300)
    Total_Production_Item=models.IntegerField(default=0)
    Production_and_Expense_Proof_Screenshot=models.ImageField(upload_to="Production_and_Expense_Proof_Screenshot")
    Total_Expense_Amount=models.IntegerField(default=0)
    Remarks_of_Expense=models.CharField(max_length=3000)
    def __str__(self) :
        return  f"{self.user.username}-{self.Puroduction_Product_Name}"
class Client(models.Model):
    user=models.ForeignKey(User,related_name="Customeer",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    profilepic=models.ImageField(upload_to='clientpic/', null=True,blank=True,default="media/Company Logo/logo1.png")
    Full_Name=models.CharField(max_length=200)
    Billing_Address=models.CharField(max_length=1000)
    City=models.CharField(max_length=500)
    State=models.CharField(max_length=500)
    Email=models.CharField(max_length=200,null=True,blank=True)
    Whats_App_Number=models.CharField(max_length=200,primary_key=True)
    Phone_Number=models.CharField(max_length=200,null=True,blank=True)
    Business_Name=models.CharField(max_length=200,null=True,blank=True)
    Acccount_Type=models.CharField(max_length=200,null=True,blank=True)
    Opening_Balance=models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True,default=0)
    Credit_Limit=models.DecimalField(max_digits=10,decimal_places=4,null=True,blank=True,default=0)
    
    def __str__(self) :

        return  f"{self.Whats_App_Number}"


class  Sale(models.Model):
    user=models.ForeignKey(User,related_name="Sale",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Client_ID=models.ForeignKey(Client,related_name="Client_ID",on_delete=models.CASCADE,null=True)
    Sale_Production_Name=models.CharField(max_length=500)
    Items_Or_Balles=models.IntegerField(default=0)
    Weight=models.DecimalField(max_digits=100,decimal_places=5,default=0)
    KG = 'KG'
    MUN = 'MUN'
    QUANTITY="QUANTITY"
    OTHERS="OTHERS"
    STATUS_CHOICES = (
        ( KG, 'KG'),
        ( MUN, ' MUN'),
        ( QUANTITY,'QUANTITY'),
        (OTHERS,"OTHERS")
    )
    Weight_Unit = models.CharField(max_length=20, choices=STATUS_CHOICES, default=MUN)
    Sale_Price=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Total_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Paid_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Payment_Status=models.BooleanField(default=False)
    Discount=models.DecimalField(max_digits=8,decimal_places=2,default=0,null=True,blank=True)
    Final_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0,null=True,blank=True)
    Remaining=models.DecimalField(max_digits=20,decimal_places=2,default=0,null=True,blank=True)
    Client_Name=models.CharField(max_length=200)
    Client_Phone_Number=models.CharField(max_length=20)
    Shiping_Address=models.CharField(max_length=1000)
    Shipping_City=models.CharField(max_length=1000)
    Shiping_State=models.CharField(max_length=1000)
    Driver_Name=models.CharField(max_length=200)
    Vehicle_Number=models.CharField(max_length=50)
    Vehicle_Weight=models.DecimalField(max_digits=100,decimal_places=5,default=0)
    VECHCLE_WEIGHT_CHOICE = (
        ( KG, 'KG'),
        ( MUN, ' MUN'),
         
    )
    VECHCLE_WEIGHT_Unit = models.CharField(max_length=20, choices=STATUS_CHOICES, default=MUN)
    Computer_Weight_Slip=models.ImageField(upload_to="Sale Splip")
    Payment_Slip=models.ImageField(upload_to="Payment Slip",blank=True,null=True)
    GST=models.DecimalField(max_digits=4,decimal_places=1,default=0,blank=True,null=True)
    Driver_Contact=models.CharField(max_length=200)
    date=models.DateField(default=timezone.now)
    
    def __str__(self) :

        return  f"{self.Client_Name}"
 

class Expense(models.Model):
    user=models.ForeignKey(User,related_name="Expenses",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('Office Supplies', 'Office Supplies'),
        ('Travel', 'Travel'),
        ('Utilities', 'Utilities'),
        ('Marketing', 'Marketing'),
        ('Other', 'Other'),
    ]

    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    Bill_Proof=models.ImageField(upload_to="Expenses Bill")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"


class PaymentOut(models.Model):
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name="Transaction",on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('Profit', 'Profit'),
        ('Travel', 'Travel'),
        ('Utilities', 'Utilities'),
        ('Marketing', 'Marketing'),
        ('Other', 'Other'),
    ]
    name=models.CharField(max_length=100)

    description = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    Bill_Proof=models.ImageField(upload_to="Expenses Bill")
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"



from django.db import models

from django.utils import timezone
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta
# Custom User Manager (Optional - if you need custom user creation logic)
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for User model
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True
    )

    business_logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    license_no = models.CharField(max_length=100, blank=True, null=True, unique=True)
    document = models.FileField(upload_to='user_documents/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()  # ✅ correct placement of manager

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

class CompanyDetail(models.Model):
    name=models.CharField(max_length=100)
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
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
    profilepic=models.ImageField(upload_to='profilepic/',default="media/img/logo1.png" ,null=True,blank=True)
    email=models.CharField(max_length=200,null=True,blank=True)
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
    PER_ACER = ' PER_ACER'
    PURCHASE_WEIGHT = ' PURCHASE_WEIGHT'
    OTHERS="OTHERS"
    PURCHASE_CHOICES = (
        (PER_ACER, ' PER_ACER'),
        (PURCHASE_WEIGHT, '  PURCHASE_WEIGHT'),
        (OTHERS,"OTHERS")
    )
    Manufacturing_Purchase_Type= models.CharField(max_length=20, choices=PURCHASE_CHOICES, default=PER_ACER)
    
    
    Supplier_Name=models.CharField(max_length=200)
    Place_Of_Supply=models.CharField(max_length=200)
    Total_Acers=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Per_Acer_Purchase_Price=models.DecimalField(max_digits=100,decimal_places=2,default=0)
     
    Weight=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Manufacture_Weight=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Estimated_weight=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Weight_After_Weight_Lose=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Weight_Lose_Value=models.IntegerField(default=0)
    Purchase_Weight_Price=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Payment_Proof=models.ImageField(upload_to="Payment Proof/",null=True,blank=True)
    Total_Production_Items=models.IntegerField(default=0)
    Manufacture_Balles=models.IntegerField(default=0)
    Total_Purchase_Price=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Purchase_Price_After_Weight_Lose=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Per_Kg_Or_Mund_Price=models.DecimalField(max_digits=100,decimal_places=2,default=0)
    Harvesting_Cost=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    WITH_FUEL= ' WITH_FUEL'
    WITHOUT_FUEL = '  WITHOUT_FUEL'
    OTHERS="OTHERS"
    HARVEST_CHOICES = (
        (WITH_FUEL, ' WITH_FUEL'),
        ( WITHOUT_FUEL, '   WITHOUT_FUEL'),
        (OTHERS,"OTHERS")
    )
    Harvest_Type= models.CharField(max_length=20, choices=HARVEST_CHOICES, default=OTHERS)
    Total_Fuel= models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Fuel_Price= models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Total_Harvest_Acer= models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Harvest_Acer_Cost= models.DecimalField(max_digits=20, decimal_places=2,default=0)
    Pressing_Cost=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Dumping_Cost=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Mud_Cost=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Polythene_Cost=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Weight_Losses=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Packing_Material=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Machine_Depreciation=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Loading_Cost=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Labour_Expense=models.DecimalField( max_digits=20,decimal_places=2,default=0)
    Other_Expense=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Manufacturing_Expense=models.IntegerField(default=0)
    Total_Sale_Amount=models.DecimalField(max_digits=20,decimal_places=2,null=True,blank=True,default=0)
    Profit_OR_Lose=models.DecimalField( max_digits=20,decimal_places=2,null=True,blank=True,default=0)
    Complete_Production=models.BooleanField(default=False)
    Out_Of_Stock=models.BooleanField(default=False)
    KG = 'KG'
    MUN = 'MUN'
    NONE='NONE'
    OTHERS="OTHERS"
    WEIGHT_CHOICES = (
        (NONE,'NONE'),
        ( KG, 'KG'),
        ( MUN, ' MUN'),
        (OTHERS,"OTHERS")
    )
    Paid_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Remaining_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Payment_Status=models.BooleanField(default=False)
    Unit = models.CharField(max_length=20, choices=WEIGHT_CHOICES, default=NONE)
    date=models.DateField(default=timezone.now)
    class Meta:
        verbose_name_plural="Manufacturing Records"
    
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
    Total_Expense_Amount=models.IntegerField(default=0)
    Remarks_of_Expense=models.CharField(max_length=3000)
    def __str__(self) :
        return  f"{self.user.username}-{self.Puroduction_Product_Name}"
def generate_unique_client_code():
    today_str = datetime.now().strftime('%Y%m%d')  # e.g. 20240619
    prefix = "CLT"
    while True:
        random_suffix = get_random_string(length=4, allowed_chars='0123456789')
        client_code = f"{prefix}-{today_str}-{random_suffix}"
        if not Client.objects.filter(Whats_App_Numbe=client_code).exists():
            return client_code
class Client(models.Model):
    user=models.ManyToManyField(User,related_name="Customeer")
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    profilepic=models.ImageField(upload_to='clientpic/', null=True,blank=True,default="media/Company Logo/logo1.png")
    Full_Name=models.CharField(max_length=200)
    Billing_Address=models.CharField(max_length=1000)
    City=models.CharField(max_length=500)
    State=models.CharField(max_length=500)
    Email=models.CharField(max_length=200,null=True,blank=True)
    Whats_App_Numbe=models.CharField(max_length=200,primary_key=True)
    Whats_App_Number=models.CharField(max_length=200,null=True,blank=True)
    Phone_Number=models.CharField(max_length=200,null=True,blank=True)
    Business_Name=models.CharField(max_length=200,null=True,blank=True)
    Acccount_Type=models.CharField(max_length=200,null=True,blank=True)
    Opening_Balance=models.DecimalField(max_digits=20,decimal_places=3,null=True,blank=True,default=0)
    Credit_Limit=models.DecimalField(max_digits=20,decimal_places=3,null=True,blank=True,default=0)
    
    class Meta:
        verbose_name_plural="Daily Production Record"
    def __str__(self) :

        return  f"{self.Whats_App_Number}"
    def save(self, *args, **kwargs):
        if not self.Whats_App_Numbe:
            self.Whats_App_Numbe = generate_unique_client_code()
        super().save(*args, **kwargs)

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
    Computer_Weight_Slip=models.ImageField(upload_to="Sale Splip",blank=True,null=True)
    Payment_Slip=models.ImageField(upload_to="Payment Slip",blank=True,null=True)
    GST=models.DecimalField(max_digits=4,decimal_places=1,default=0,blank=True,null=True)
    Driver_Contact=models.CharField(max_length=200)
    CREDIT = 'CREDIT'
    CASH = 'CASH'
    OTHERS="OTHERS"
    STATUS_CHOICES = (
        ( CREDIT, 'CREDIT'),
        ( CASH , ' CASH '),
        (OTHERS,"OTHERS")
    )
    Payment_Method = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CASH)
    date=models.DateField(default=timezone.now)
    class Meta:
        verbose_name_plural="Sales Record"
    
    def __str__(self) :

        return  f"{self.Client_Name}"
 

class Expense(models.Model):
    user=models.ForeignKey(User,related_name="Expenses",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Production_Name=models.CharField(max_length=100, null=True)
    CATEGORY_CHOICES = [
        ('Harvesting', 'Harvesting'),
        ('Pressing', 'Pressing'),
        ('Dumping', 'Dumping'),
        ('Polythene', 'Polythene'),
        ('Mud Cost', 'Mud Cost'),
        ('Weight Losses', 'Weight Losses'),
        ('Balling Paper', 'Balling Paper'),
        ('Stitch Paper', ' Stitch Paper'),
        ('Machine Depreciation', 'Machine Depreciation'),
        ('Loading', 'Loading'),
        ('Labour', 'Labour'),
        ('Office Supplies', 'Office Supplies'),
        ('Travel', 'Travel'),
        ('Utilities', 'Utilities'),
        ('Marketing', 'Marketing'),
        ('Other', 'Other'),
    ]


    description = models.CharField(max_length=255,blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    Paid_Amount=models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True,default=0)
    Remaining_Amount=models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True,default=0)
    date = models.DateField(default=timezone.now)
    Bill_Proof=models.ImageField(upload_to="Expenses Bill",blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    PAYMENT_CHOICES = [
        ('CREDIT', 'CREDIT'),
        ('PAID', 'PAID'),
         
    ]
     
    Payment_Status= models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='PAID')
    class Meta:
        verbose_name_plural="Expenses"

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

    class Meta:
        verbose_name_plural="Transactions"

    def __str__(self):
        return f"{self.description} - {self.amount}"
class Sale_Return(models.Model):
    user=models.ForeignKey(User,related_name="Return",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Client_ID=models.ForeignKey(Client,related_name="Customer",on_delete=models.CASCADE,null=True)
    Client_Name=models.CharField(max_length=500)
    Sale_Production_Name=models.CharField(max_length=500)
    Items_Or_Balles=models.IntegerField(default=0)
    Weight=models.DecimalField(max_digits=100,decimal_places=5,default=0)
    Return_To_Customer_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Payment_Proof=models.ImageField(upload_to="Return Payment Proof")
    Reason_Of_Return=models.TextField()
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural="Sales Returns"
    
    def __str__(self):
        return f"{self.Client_Name} - {self.Return_To_Customer_Amount}"
class Production_Labour(models.Model):
    user=models.ForeignKey(User,related_name="ProductionLabour",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Team_Leader=models.CharField(max_length=500)
    Credit=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Paid=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Advance=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Bales=models.DecimalField(max_digits=20,decimal_places=2,default=0)

    class Meta:
        verbose_name_plural="Productions Labours"
    def __str__(self):
        return f"{self.Team_Leader}"
class Loading_Labour(models.Model):
    user=models.ForeignKey(User,related_name="LoadingLabour",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Team_Leader=models.CharField(max_length=500)
    Credit=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Paid=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Advance=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Bales=models.DecimalField(max_digits=20,decimal_places=2,default=0)

    class Meta:
        verbose_name_plural="Loading Labours"
    def __str__(self):
        return f"{self.Team_Leader}"
class ProducctionLabourRecord(models.Model):
    user=models.ForeignKey(User,related_name="ProductionRecord",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Team_Leader=models.CharField(max_length=500)
    Labour_Id=models.IntegerField(default=0)
    Bankar=models.CharField(max_length=500)
    Credit=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Bales=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Per_Bale_Price=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Total_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Paid_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Remaining=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    date = models.DateField(default=timezone.now)
    PAYMENT_CHOICES = [
        ('CREDIT', 'CREDIT'),
        ('PAID', 'PAID'),
         
    ]
     
    Payment_Status= models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='PAID')

    class Meta:
        verbose_name_plural="Production Labours Record"

    def __str__(self):
        return f"{self.Team_Leader}-{self.Bales}"


class LoadingLabourRecord(models.Model):
    user=models.ForeignKey(User,related_name="LoadingRecord",on_delete=models.CASCADE)
    userprofile  = models.ForeignKey(Profile,blank=True, null=True, on_delete=models.CASCADE)
    Team_Leader=models.CharField(max_length=500)
    Labour_Id=models.IntegerField(default=0)
    Bankar=models.CharField(max_length=500)
    Credit=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Paid=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Bales=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Per_Bale_Price=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Total_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Paid_Amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    Remaining=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    date = models.DateField(default=timezone.now)
    PAYMENT_CHOICES = [
        ('CREDIT', 'CREDIT'),
        ('PAID', 'PAID'),
         
    ]
     
    Payment_Status= models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='PAID')
    class Meta:
        verbose_name_plural="Loadings Labours Record"

    def __str__(self):
        return f"{self.Team_Leader}-{self.Bales}"
class Loading_Labour_Advance_Payment(models.Model):
    user=models.ForeignKey(User,related_name="LoadingLabourAdvance",on_delete=models.CASCADE)
    Team_Leader=models.CharField(max_length=500)
    Advance=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    date=models.DateField(default=timezone.now)
    class Meta:
        verbose_name_plural="Loading Labour Advance Payment"
    def __str__(self):
        return f"{self.Team_Leader}-{self.Advance}"
class Production_Labour_Advance_Payment(models.Model):
    user=models.ForeignKey(User,related_name="ProductionLabourAdvance",on_delete=models.CASCADE)
    Team_Leader=models.CharField(max_length=500)
    Advance=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    date=models.DateField(default=timezone.now)
    class Meta:
        verbose_name_plural="Production Labour Advance Payment"
    def __str__(self):
        return f"{self.Team_Leader}-{self.Advance}"
class OTPRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_records')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return self.created_at < timezone.now() - timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.email} - {self.otp_code}"
 

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    )
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.PositiveIntegerField()
    max_users = models.PositiveIntegerField(null=True, blank=True)  # None = unlimited
    max_clients = models.PositiveIntegerField(null=True, blank=True)
    features = models.TextField()
    duration_days = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.name} - PKR {self.price}"

from django.conf import settings
class UserSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    transaction_token = models.CharField(max_length=200, null=True, blank=True)

    def activate(self):
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        self.is_active = True
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Subscription: {self.plan.name}"


                
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import *
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin interface for CustomUser model"""
    
    # Fields to display in the admin list view
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'phone_number', 'license_no', 'is_verified', 
        'is_staff', 'date_joined'
    )
    
    # Fields that can be used for filtering
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 
        'is_verified', 'date_joined', 'last_login'
    )
    
    # Fields that can be searched
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'license_no')
    
    # Ordering
    ordering = ('-date_joined',)
    
    # Fields to display in the admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Business Information', {
            'fields': ('company_name','phone_number', 'business_logo', 'license_no', 'document','business_address')
        }),
        ('Additional Info', {
            'fields': ('is_verified', 'created_at', 'updated_at')
        }),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Business Information', {
            'fields': ('phone_number', 'business_logo', 'license_no', 'document')
        }),
        ('Additional Info', {
            'fields': ('is_verified',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login')
    
    def get_readonly_fields(self, request, obj=None):
        """Make timestamp fields read-only"""
        if obj:  # Editing an existing object
            return self.readonly_fields + ('username',)
        return self.readonly_fields

class ManufacturingInline(admin.TabularInline):
    model = Manufacturing
    extra = 0 
class DailyProductionInline(admin.TabularInline):
    model = DailyProduction
    extra = 0 
class ClientInline(admin.TabularInline):
    model = Client
    extra = 0 
class SaleInline(admin.TabularInline):
    model = Sale
    extra = 0 
class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0 
class PayemtoutInline(admin.TabularInline):
    model = PaymentOut
    extra = 0 
class SaleReturnInline(admin.TabularInline):
    model = Sale_Return
    extra = 0 




class SaleLine(admin.ModelAdmin):
    inlines = [SaleInline]
   
class ProfileAdmin(admin.ModelAdmin):
    inlines = [DailyProductionInline,ClientInline,SaleInline,ManufacturingInline,ExpenseInline,PayemtoutInline,SaleReturnInline]
    search_fields=['Sale_Production_Name']

admin.site.register(CompanyDetail)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Manufacturing)
admin.site.register(DailyProduction) 
admin.site.register(Client,SaleLine)
admin.site.register(Sale)
admin.site.register(Expense)
admin.site.register(PaymentOut)
admin.site.register(Sale_Return)
admin.site.register(Production_Labour)
admin.site.register(ProducctionLabourRecord)
admin.site.register(Loading_Labour)
admin.site.register(LoadingLabourRecord)
admin.site.register(Loading_Labour_Advance_Payment)
admin.site.register(Production_Labour_Advance_Payment)
admin.site.register(OTPRecord)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionPlan)

admin.site.site_header = "SoftApex Technologies"
admin.site.site_title = "SoftApex Technologies"
admin.site.index_title = "Welcome SoftApex Technologies Admin"

# Register your models here.

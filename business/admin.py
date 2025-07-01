from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'phone_number', 'license_no', 'is_verified',
        'is_staff', 'date_joined'
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active',
        'is_verified', 'date_joined', 'last_login'
    )
    search_fields = (
        'username', 'first_name', 'last_name',
        'email', 'phone_number', 'license_no'
    )
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Business Information', {
            'fields': ('company_name', 'phone_number', 'business_logo',
                       'license_no', 'document', 'business_address')
        }),
        ('Additional Info', {
            'fields': ('is_verified', 'created_at', 'updated_at')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Business Information', {
            'fields': ('phone_number', 'business_logo', 'license_no', 'document')
        }),
        ('Additional Info', {
            'fields': ('is_verified',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('username',)
        return self.readonly_fields

# ✅ Register all models directly — no inlines
admin.site.register(CompanyDetail)
admin.site.register(Profile)
admin.site.register(Manufacturing)
admin.site.register(DailyProduction)
admin.site.register(Client)
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

# ✅ Admin branding
admin.site.site_header = "SoftApex Technologies"
admin.site.site_title = "SoftApex Technologies"
admin.site.index_title = "Welcome SoftApex Technologies Admin"

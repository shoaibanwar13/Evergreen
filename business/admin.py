from django.contrib import admin

from .models import *
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




class SaleLine(admin.ModelAdmin):
    inlines = [SaleInline]
   
class ProfileAdmin(admin.ModelAdmin):
    inlines = [DailyProductionInline,ClientInline,SaleInline,ManufacturingInline,ExpenseInline,PayemtoutInline]
    search_fields=['Sale_Production_Name']

admin.site.register(CompanyDetail)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Manufacturing)
admin.site.register(DailyProduction) 
admin.site.register(Client,SaleLine)
admin.site.register(Sale)
admin.site.register(Expense)
admin.site.register(PaymentOut)


# Register your models here.

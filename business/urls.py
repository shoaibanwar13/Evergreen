
from django.urls import path
from.views import *
from django.contrib.auth import views
urlpatterns = [
    path("",index,name="index"),
    path("Addclient/",Addclient,name="Addclient"),
    path("Vendor/",Vendor,name="Vendor"),
    path("AddDailyProduction/",AddDailyProduction,name="AddDailyProduction"),
    path("Client_Whatsapp_filter/",Client_Whatsapp_filter,name="Client_Whatsapp_filter"),
    path("Client_mobileno_filter/",Client_mobileno_filter,name="Client_mobileno_filter"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('check_product_name/', check_product_name, name='check_product_name'),
    path('NewPurchasepdf/', NewPurchasepdf, name='NewPurchasepdf'),
    path('TotalVendorPurchase/', TotalVendorPurchase, name='TotalVendorPurchase'),
    path('purchase_export_to_excel/', purchase_export_to_excel, name='purchase_export_to_excel'),
    path('current_purchase_pdf/', current_purchase_pdf, name='current_purchase_pdf'),
    path('Purchase_Search_and_manage/',Purchase_Search_and_manage,name="Purchase_Search_and_manage"),
    path('VendorPurchaseSearch/',VendorPurchaseSearch,name="VendorPurchaseSearch"),
    path('VendorClientSearch/',VendorClientSearch,name="VendorClientSearch"),
    path('ClientProfile/<str:pk>/',ClientProfile,name="ClientProfile"),
    path('ManufactureMaterialPurchase/',ManufactureMaterialPurchase,name="ManufactureMaterialPurchase"),
    path('ManufacturePuchasePDF/',ManufacturePuchasePDF,name="ManufacturePuchasePDF"),
    path('ManufactureMaterrial_export_to_excel/',ManufactureMaterrial_export_to_excel,name="ManufactureMaterrial_export_to_excel")
    

]

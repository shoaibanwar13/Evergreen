
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
    path('ManufactureMaterrial_export_to_excel/',ManufactureMaterrial_export_to_excel,name="ManufactureMaterrial_export_to_excel"),
    path('SalewithClient/',SalewithClient,name='SalewithClient'),
    path('SaleGenerate/',SaleGenerate,name='SaleGenerate'), 
    path('client_search/',client_search,name='client_search'),
    path('CurrentSale/<str:pk>/',CurrentSale,name='CurrentSale'),
    path('currentInvoice/<str:pk>/',currentInvoice,name='currentInvoice'),
    path('ClientSearchAndPurchase/<str:pk>/',ClientSearchAndPurchase,name='ClientSearchAndPurchase'),
    path('ClientReport/<str:pk>/',ClientReport,name='ClientReport'),
    path('Client_export_to_excel/<str:pk>/',Client_export_to_excel,name='Client_export_to_excel'),
    path('SaleManagement/',SaleManagement,name='SaleManagement'),
    path('SaleReport/',SaleReport,name='SaleReport'),
    path('VendorSale_export_to_excel/',VendorSale_export_to_excel,name='VendorSale_export_to_excel'),
    path('paymentIn/<str:pk>/<str:id>/',paymentIn,name='paymentIn'),
    path('Itemchecking/',Itemchecking,name='Itemchecking'),
    path('currentPaymentInPdf/<str:pk>/<str:id>/',currentPaymentInPdf,name='currentPaymentInPdf'), 
    path('paymentInSlip/<str:pk>/<str:id>/',paymentInSlip,name='paymentInSlip'),
    path('add_expense/', add_expense, name='add_expense'),
    path('expenseManagement/', expenseManagement, name='expenseManagement'),
    path('generate_expense_report/', generate_expense_report, name='generate_expense_report'),
    path('expensebill/', expensebill, name='expensebill'),
    path('ExpenseSlip/', ExpenseSlip, name='ExpenseSlip'),
    path('expense_Excel/', expense_Excel, name='expense_Excel'),
    path('VendorPayementOut/', VendorPayementOut, name='VendorPayementOut'),
    path('withdrwalSlip/', withdrwalSlip, name='withdrwalSlip'), 
    path('PaymentOutSlip/', PaymentOutSlip, name='PaymentOutSlip'),
    path('transactionHistory/', transactionHistory, name='transactionHistory'),
    path('generate_Transactions_report/',  generate_Transactions_report, name=' generate_Transactions_report'),
    path('search/',search, name='search'), 
    path('Salereturn/',Salereturn, name='Salereturn'),
    path('SaleReturnManagement/',SaleReturnManagement, name='SaleReturnManagement'), 
    path('VendorSaleReturn_export_to_excel/',VendorSaleReturn_export_to_excel, name='VendorSaleReturn_export_to_excel'),
    path('SaleReturnReport/',SaleReturnReport, name='SaleReturnReport'),
    path('AddManufecturePurchase/',AddManufecturePurchase, name='AddManufecturePurchase'),
    path('Dumping/', Dumping, name=' Dumping'),
    path('HarvestingExpense/',HarvestingExpense, name='HarvestingExpense'),
    path('Polythene/',Polythene, name='Polythene'),
    path('PackingMaterial/', PackingMaterial, name=' PackingMaterial'),
    path('WeightLose/', WeightLose, name=' WeightLose'),
    path('add_production_labour/', add_production_labour, name=' add_production_labour'),
    path('add_loading_labour/', add_loading_labour, name=' add_loading_labour'),
    path('add_loading_labour_record/', add_loading_labour_record, name=' add_loading_labour_record'),
    path('search1/', search1, name=' search1'),
    path('generate_Production_Labour_report/', generate_Production_Labour_report, name=' generate_Production_Labour_report'),
    path('Production_Labour_Excel/', Production_Labour_Excel, name='Production_Labour_Excel'),
    path('search2/', search2, name=' search2'),
    path('generate_Loading_Labour_report/', generate_Loading_Labour_report, name=' generate_Loading_Labour_report'),
    path('Loading_Labour_Excel/', Loading_Labour_Excel, name='Loading_Labour_Excel'),
    path('CreditToPaid/<str:id>/',CreditToPaid,name='CreditToPaid'),
    path('CreditToPaidLoading/<str:id>/',CreditToPaidLoading,name='CreditToPaidLoading'),
    path('BunkarExpense/<str:id>/',BunkarExpense,name='BunkarExpense'),
    path('fetch_details/<str:bunkar>/',fetch_details,name="fetch_details"),
    path('Estimater/',Estimater,name="Estimater"),
    path('Production_Labour_Advance_Payment/',Production_Labour_Advance,name='Production_Labour_Advance'),
    path('Loading_Labour_Advance_Payment/',Loading_Labour_Advance,name='Loading_Labour_Advance')
    
    
     
    
     
    

    
  
    
    

]

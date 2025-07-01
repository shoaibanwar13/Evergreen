from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.db.models import F
from weasyprint import HTML
from django.contrib.auth.decorators import login_required
import os
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from django.urls import reverse
import random
from datetime import date
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
import pandas as pd
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
from django.core.mail import EmailMessage
from .models import *
from datetime import datetime
from decimal import Decimal
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.decorators.csrf import csrf_exempt  # If needed for testing
from django.views.decorators.http import require_POST
import weasyprint
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum, F, ExpressionWrapper
def index(request):
    compydetail=CompanyDetail.objects.all()
    plans = SubscriptionPlan.objects.all()
    return render(request,"index.html", {'compydetail':compydetail,"plans":plans})
def calculate_monthly_total(request,year, month):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    total = Manufacturing.objects.filter(user=request.user,date__gte=start_date, date__lt=end_date)
    total_purchase=Decimal(0.00)
    for vtotal in total:
        total_purchase+=vtotal.Total_Purchase_Price
        
    return total_purchase or 0
def calculate_monthly_Sale(request, year, month):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    total = Manufacturing.objects.filter(user=request.user, date__gte=start_date, date__lt=end_date)
    total_purchase = Decimal(0.00)

    for vtotal in total:
        total_purchase += vtotal.Total_Sale_Amount or Decimal(0.00)
        

    return total_purchase or Decimal(0.00)
def calculate_monthly_Pending(request,year, month):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    total = Sale.objects.filter(user=request.user,date__gte=start_date, date__lt=end_date)
    total_purchase=Decimal(0.00)
    for vtotal in total:
        total_purchase+=vtotal.Remaining
         
    return total_purchase or 0
def calculate_monthly_received(request,year, month):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    total = Sale.objects.filter(user=request.user,date__gte=start_date, date__lt=end_date)
    total_purchase=Decimal(0.00)
    for vtotal in total:
        total_purchase+=vtotal.Paid_Amount
         
    return total_purchase or 0
@login_required
def Vendor(request):
   
    current_year = datetime.now().year
    recent_sales = Sale.objects.filter(user=request.user).order_by('-date')[:10]
    january_total = february_total = march_total = april_total = may_total = june_total = 0
    july_total = august_total = september_total = october_total = november_total = december_total = 0
    january_total = calculate_monthly_total(request,current_year, 1)
    february_total = calculate_monthly_total(request,current_year, 2)
    march_total = calculate_monthly_total(request,current_year, 3)
    april_total = calculate_monthly_total(request,current_year, 4)
    may_total = calculate_monthly_total(request,current_year, 5)
    june_total = calculate_monthly_total(request,current_year, 6)
    july_total = calculate_monthly_total(request,current_year, 7)
    august_total = calculate_monthly_total(request,current_year, 8)
    september_total = calculate_monthly_total(request,current_year, 9)
    october_total = calculate_monthly_total(request,current_year, 10)
    november_total = calculate_monthly_total(request,current_year, 11)
    december_total = calculate_monthly_total(request,current_year, 12)
    january_Sale= calculate_monthly_Sale(request,current_year, 1)
    february_Sale= calculate_monthly_Sale(request,current_year, 2)
    march_Sale= calculate_monthly_Sale(request,current_year, 3)
    april_Sale= calculate_monthly_Sale(request,current_year, 4)
    may_Sale= calculate_monthly_Sale(request,current_year, 5)
    june_Sale= calculate_monthly_Sale(request,current_year, 6)
    july_Sale= calculate_monthly_Sale(request,current_year, 7)
    august_Sale= calculate_monthly_Sale(request,current_year, 8)
    september_Sale= calculate_monthly_Sale(request,current_year, 9)
    october_Sale= calculate_monthly_Sale(request,current_year, 10)
    november_Sale= calculate_monthly_Sale(request,current_year, 11)
    december_Sale= calculate_monthly_Sale(request,current_year, 12)
    january_received= calculate_monthly_received(request,current_year, 1)
    february_received= calculate_monthly_received(request,current_year, 2)
    march_received= calculate_monthly_received(request,current_year, 3)
    april_received= calculate_monthly_received(request,current_year, 4)
    may_received= calculate_monthly_received(request,current_year, 5)
    june_received= calculate_monthly_received(request,current_year, 6)
    july_received= calculate_monthly_received(request,current_year, 7)
    august_received= calculate_monthly_received(request,current_year, 8)
    september_received= calculate_monthly_received(request,current_year, 9)
    october_received= calculate_monthly_received(request,current_year, 10)
    november_received= calculate_monthly_received(request,current_year, 11)
    december_received= calculate_monthly_received(request,current_year, 12)
    january_pending= calculate_monthly_Pending(request,current_year, 1)
    february_pending= calculate_monthly_Pending(request,current_year, 2)
    march_pending= calculate_monthly_Pending(request,current_year, 3)
    april_pending= calculate_monthly_Pending(request,current_year, 4)
    may_pending= calculate_monthly_Pending(request,current_year, 5)
    june_pending= calculate_monthly_Pending(request,current_year, 6)
    july_pending= calculate_monthly_Pending(request,current_year, 7)
    august_pending= calculate_monthly_Pending(request,current_year, 8)
    september_pending= calculate_monthly_Pending(request,current_year, 9)
    october_pending= calculate_monthly_Pending(request,current_year, 10)
    november_pending= calculate_monthly_Pending(request,current_year, 11)
    december_pending= calculate_monthly_Pending(request,current_year, 12)
    
    
                                
    user=request.user             
    # Consolidated queryset filters
    manufacturings = Manufacturing.objects.filter(user=user)
    sales = Sale.objects.filter(user=user)
    withdrawals = PaymentOut.objects.filter(user=user)
    loading_labour_credit = LoadingLabourRecord.objects.filter(user=user, Payment_Status="CREDIT")
    production_labour_credit = ProducctionLabourRecord.objects.filter(user=user, Payment_Status="CREDIT")
    expenses_credit = Expense.objects.filter(user=user, Payment_Status="CREDIT")
    manufacturing_credit = Manufacturing.objects.filter(user=user, Payment_Status=False)

    # Aggregations
    total_purchase = manufacturings.aggregate(total=Sum('Total_Purchase_Price'))['total'] or Decimal(0.00)
    total_sale = manufacturings.aggregate(total=Sum('Total_Sale_Amount'))['total'] or Decimal(0.00)
    manufacture_expense = manufacturings.aggregate(total=Sum('Manufacturing_Expense'))['total'] or Decimal(0.00)

    total_sales = sales.aggregate(total=Sum('Total_Amount'))['total'] or Decimal(0.00)
    total_pending = sales.aggregate(total=Sum('Remaining'))['total'] or Decimal(0.00)
    total_Recived_Payment = sales.aggregate(total=Sum('Paid_Amount'))['total'] or Decimal(0.00)

    siteexp = withdrawals.aggregate(total=Sum('amount'))['total'] or Decimal(0.00)

    # Profit calculation
    profit = total_sale - total_purchase - manufacture_expense
    siteProfit = profit - siteexp

    # Credit calculations
    Creditamount = loading_labour_credit.aggregate(total=Sum('Remaining'))['total'] or Decimal(0.00)
    CreditamountPro = production_labour_credit.aggregate(total=Sum('Remaining'))['total'] or Decimal(0.00)
    Expense_Credit = expenses_credit.aggregate(total=Sum('Remaining_Amount'))['total'] or Decimal(0.00)
    Manufacturing_Credit = manufacturing_credit.aggregate(total=Sum('Remaining_Amount'))['total'] or Decimal(0.00)
        
    context={
        'total_purchase':total_purchase,
        'total_sales':total_sales,
        'total_pending':total_pending,
        'total_Recived_Payment':total_Recived_Payment,
        'siteexp':siteexp,
        'manufacture_expense':manufacture_expense,
        'siteProfit':siteProfit,
        'january_total': january_total,
        'february_total': february_total,
        'march_total': march_total,
        'april_total': april_total,
        'may_total': may_total,
        'june_total': june_total,
        'july_total': july_total,
        'august_total': august_total,
        'september_total': september_total,
        'october_total': october_total,
        'november_total': november_total,
        'december_total': december_total,
        'january_Sale': january_Sale,
        'february_Sale': february_Sale,
        'march_Sale': march_Sale,
        'april_Sale': april_Sale,
        'may_Sale': may_Sale,
        'june_Sale': june_Sale,
        'july_Sale': july_Sale,
        'august_Sale': august_Sale,
        'september_Sale': september_Sale,
        'october_Sale': october_Sale,
        'november_Sale': november_Sale,
        'december_Sale': december_Sale,
        'january_received': january_received,
        'february_received': february_received,
        'march_received': march_received,
        'april_received': april_received,
        'may_received': may_received,
        'june_received': june_received,
        'july_received': july_received,
        'august_received': august_received,
        'september_received': september_received,
        'october_received': october_received,
        'november_received': november_received,
        'december_received': december_received,
        
        'january_pending': january_pending,
        'february_pending': february_pending,
        'march_pending': march_pending,
        'april_pending': april_pending,
        'may_pending': may_pending,
        'june_pending': june_pending,
        'july_pending': july_pending,
        'august_pending': august_pending,
        'september_pending': september_pending,
        'october_pending': october_pending,
        'november_pending': november_pending,
        'december_pending': december_pending,
        'Creditamount':Creditamount,
        'CreditamountPro': CreditamountPro,
        'Expense_Credit':Expense_Credit,
        'Manufacturing_Credit':Manufacturing_Credit,
        'recent_sales':recent_sales
        
        
    }
    

   
    if request.htmx:
        return render(request, 'components/Vendor.html',context)
    else:

      return render(request,"Vendor.html",context)
@login_required
def Addclient(request):
    compydetail=CompanyDetail.objects.filter(user=request.user).first()
    if request.method=="POST":
        name=request.POST.get("fullname")
        email=request.POST.get("email")
        whatsappno=request.POST.get("WhatsAppNo")
        phoneno=request.POST.get("mnumber")
        clientPic=request.FILES['pic']
        address=request.POST.get("address")
        city=request.POST.get("city")
        state=request.POST.get("state")
        bname=request.POST.get("bname")
        accountType=request.POST.get("accountType")
        openingBalance=Decimal(request.POST.get("openbalance",''))
        creditlimit=Decimal(request.POST.get("creditLimit",''))
        profile_instance= get_object_or_404(Profile, user=request.user)
        query=Client.objects.create(userprofile=profile_instance,Full_Name=name,Email=email,Whats_App_Number=whatsappno,Phone_Number=phoneno,Billing_Address=address,City=city,State=state,Business_Name=bname,Acccount_Type=accountType,Opening_Balance=openingBalance,Credit_Limit=creditlimit,profilepic=clientPic)
        query.user.add(request.user)
        query.save()
        return redirect("SaleGenerate")
    if request.htmx:
        return render(request, 'components/AddClient.html',{'compydetail': compydetail})
    else:
        return render(request,"client.html",{'compydetail': compydetail})
     

@login_required
def AddDailyProduction(request):
    labour=Production_Labour.objects.filter(user=request.user)
    Products=Manufacturing.objects.filter(user=request.user,Complete_Production=False).all()
    if request.method=="POST":
        Puroduction_Product_Name=request.POST.get("Production_Product_Name")
        print(Puroduction_Product_Name)
        Production_Place=request.POST.get("Production_Place")
        city=request.POST.get("City")
        Total_Production_Item=request.POST.get("Total_Production_Item")
        Production_Team_Name=request.POST.get("team")
        Total_Expense_Amount=Decimal(request.POST.get("Total_Amount"))
        Expense_Remarks=request.POST.get("Remarks_of_Expense")
        Production_completed=request.POST.get("Settlement")
        one_bale_price=request.POST.get("Bale_Production_Price")
        payment_status=request.POST.get("Payment_Status")
        paid_amount=request.POST.get('Paid_Amount')
        remaining=request.POST.get('Remaining')
        print(paid_amount,remaining)
        if not paid_amount:  # Check if the value is empty or None
            paid_amount = Decimal('0.0')
        else:
            paid_amount = Decimal(paid_amount)
        # Handling Remaining Amount
         
        if not remaining:  # Check if the value is empty or None
            remaining = Decimal('0.0')
        else:
            remaining = Decimal(remaining)
        account=Production_Labour.objects.get(user=request.user,id=Production_Team_Name)
        update=Production_Labour.objects.filter(user=request.user,id=Production_Team_Name)
        profile_instance = Profile.objects.get(user=request.user)
        query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=Puroduction_Product_Name,category="Labour",amount=Total_Expense_Amount,Payment_Status=payment_status,Paid_Amount=paid_amount,Remaining_Amount=remaining)
        query.save()
        manufaccture_instance=Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=Puroduction_Product_Name)
        manufaccture_instance.update(Labour_Expense=F("Labour_Expense")+Total_Expense_Amount)
        if payment_status=="CREDIT":
             update.update(Credit=F("Credit")+remaining,Paid=F("Paid")+paid_amount,Bales=F("Bales")+Total_Production_Item)
        else:
             update.update(Paid=F("Paid")+ Total_Expense_Amount,Bales=F("Bales")+Total_Production_Item)
        # Create and save a new LoadingLabourRecord instance
        ProducctionLabourRecord.objects.create(
            user=request.user,
            userprofile=profile_instance,
            Team_Leader=account.Team_Leader,
            Bankar=Puroduction_Product_Name,
            Bales=Total_Production_Item,
            Per_Bale_Price=one_bale_price,
            Total_Amount=Total_Expense_Amount,
            Paid_Amount=paid_amount,
            Credit=remaining,
            Remaining=remaining,
            Payment_Status=payment_status,
            Labour_Id=Production_Team_Name
        )
        
        

        profile_instance= get_object_or_404(Profile, user=request.user)
        query=DailyProduction.objects.create(user=request.user,userprofile=profile_instance, Puroduction_Product_Name=Puroduction_Product_Name,Production_Place=Production_Place, City=city,Total_Production_Item=Total_Production_Item, Production_Team_Name= account.Team_Leader,Total_Expense_Amount=Total_Expense_Amount,Remarks_of_Expense=Expense_Remarks )
        query.save()
        expense=Decimal(Total_Expense_Amount)
        expenseinprofile=Profile.objects.get(user=request.user)
        expenseinprofile.Total_Expense+=expense
        expenseinprofile.save()
        items=int(Total_Production_Item)
        expense=int(Total_Expense_Amount)
        if  Production_completed=="complete":
            Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=Puroduction_Product_Name).update(
            Complete_Production=True

    )
        Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=Puroduction_Product_Name).update(
        Total_Production_Items=F('Total_Production_Items') + items,Manufacturing_Expense=F('Manufacturing_Expense')+expense,
        Manufacture_Balles=F("Manufacture_Balles")+items,Labour_Expense=F("Labour_Expense")+expense

    )
         

        
        messages.success(request, "Daily Production And Labour data added successfully!")
        return redirect("current_purchase_pdf")
    if request.htmx:
        return render(request, 'components/AddPurchase.html',{ 'Products': Products,'labour':labour})
    else:
        return render(request,"Addpurchase.html",{ 'Products': Products,'labour':labour})
@login_required
def Client_Whatsapp_filter(request):
    Client_Whatsapp=request.POST.get('WhatsAppNo')
    if Client.objects.filter(user=request.user,Whats_App_Number= Client_Whatsapp).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
@login_required
def Client_mobileno_filter(request):
    Mobile=request.POST.get('mnumber')
    if Client.objects.filter(user=request.user,Phone_Number=Mobile).exists():
       return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
@login_required
def check_product_name(request):
    product_name = request.GET.get('Product_Name', None)
    if product_name:
        exists = Manufacturing.objects.filter(Manufacturing_Product_Name=product_name).exists()
        print(exists)
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})
 

@login_required
def NewPurchasepdf(request):
    if not request.user.is_authenticated:
        return HttpResponse("You need to log in to view this page.", status=401)

     
    purchase = DailyProduction.objects.filter(user=request.user).last()

    if not purchase:
        return HttpResponse("No production record found.", status=404)

    html_string = render_to_string('pdfs/production_proof_slip.html', {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        'Date': datetime.now().strftime("%d/%m/%Y"),
        'ProductionCity': purchase.City,
        'ProductionPlace': purchase.Production_Place,
        'purchase': purchase,
    })

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="production_proof_slip.pdf"'
    return response
 
@login_required
def TotalVendorPurchase(request):
     
    purchase = DailyProduction.objects.filter(user=request.user)
    Total_Point_Production = purchase.count()
    Expense_Amount = Decimal(0.00)
    for purchases in purchase:
        Expense_Amount += purchases.Total_Expense_Amount

    Grand_Total = Expense_Amount
    Date = datetime.now().strftime("%d/%m/%Y")

    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "Date": Date,
        "Total_Amount": Grand_Total,
        "vendor_total_Production": Total_Point_Production,
        "purchase_list": purchase,
        "user": request.user
    }

    html_string = render_to_string('pdfs/vendor_purchase_report.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="VendorProductionReport.pdf"'
    return response
@login_required
def purchase_export_to_excel(request):
    # Query the database
    data = DailyProduction.objects.filter(user=request.user).values()
    df = pd.DataFrame(list(data))

    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=total_purchase_data.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def current_purchase_pdf(request):
    return render(request,'purchasepdf.html')
@login_required
def Purchase_Search_and_manage(request):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = DailyProduction.objects.filter(user=request.user)
    # Apply additional filters if they are provided
    if query:
        results = results.filter(Puroduction_Product_Name__icontains=query)
    if query2:
        results = results.filter(Production_Place__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)    
    if request.htmx:
        return render(request, 'components/purchase_search.html',{'results':results,'query':query,'query2':query2,'fromdate':fromdate,'todate':todate})
    else:
       return render(request,'purchase_manage.html',{'results':results,'query':query,'query2':query2,'fromdate':fromdate,'todate':todate})
@login_required
def Purchase_Filter(request):
    query = request.GET.get('query')
    results =  DailyProduction.objects.filter(Product_Name__icontains=query)
    return render(request,'PurchaseFilter.html',{'results':results,'query':query})
@login_required
def VendorPurchaseSearch(request):
    query = request.GET.get("query")
    query2 = request.GET.get("query2")
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get("todate")

    purchase = DailyProduction.objects.filter(user=request.user)
    if query:
        purchase = purchase.filter(Puroduction_Product_Name__icontains=query)
    if query2:
        purchase = purchase.filter(Production_Place__icontains=query2)
    if fromdate and todate:
        purchase = purchase.filter(date__lte=todate, date__gte=fromdate)

  

    Expense_Amount = Decimal(0.00)
    for purchases in purchase:
        Expense_Amount += purchases.Total_Expense_Amount

    Grand_Total = Expense_Amount

    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Total_Amount": Grand_Total,
        "purchase_list": purchase,
        'vendor_total_Production': purchase.count(),
        "user": request.user
    }

    html_string = render_to_string('pdfs/vendor_purchase_report.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="DailyProductionReport.pdf"'
    return response

@login_required
def ManufactureMaterialPurchase(request):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = Manufacturing.objects.filter(user=request.user)
    print(results)
    # Apply additional filters if they are provided
    if query:
        results = results.filter(Manufacturing_Product_Name__icontains=query)
    if query2:
        results = results.filter(Place_Of_Supply__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate) 
    
    if request.htmx:
       return render(request,'components/ManufactureSearching.html',{'results':results,'query':query,'query2':query2,'fromdate':fromdate,'todate':todate})
    else:
        return render(request,'MaterialPurchase.html',{'results':results,'query':query,'query2':query2,'fromdate':fromdate,'todate':todate})
@login_required
def VendorClientSearch(request):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    results = Client.objects.filter(user=request.user)

    # Apply additional filters if they are provided
    if query:
        results = results.filter(Full_Name__icontains=query)
    if query2:
        results = results.filter(Whats_App_Number__icontains=query2)
    if request.htmx:
        return render(request, 'components/SearchAndManageClient.html',{'query':query,'query2':query2,'results':results} )
    else:
      return render(request,"ManageClient.html",{'query':query,'query2':query2,'results':results})
@login_required
def ManufactureMaterrial_export_to_excel(request):
    # Query the database
    data = Manufacturing.objects.filter(user=request.user).values()
    df = pd.DataFrame(list(data))

    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Total_Manufacture_Material_data.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def ManufacturePuchasePDF(request):
    query = request.GET.get("query")
    query2 = request.GET.get("query2")
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get("todate")

    results = Manufacturing.objects.filter(user=request.user)
    if query:
        results = results.filter(Manufacturing_Product_Name__icontains=query)
    if query2:
        results = results.filter(Place_Of_Supply__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__gte=fromdate, date__lte=todate)

    

    Expense_Amount = sum([item.Manufacturing_Expense for item in results])
    Total_Purchase = sum([item.Total_Purchase_Price for item in results])
    Total_Sale = sum([item.Total_Sale_Amount for item in results])

    Grand_Total_Expense = Expense_Amount
    Grand_Total_Purchase = Total_Purchase
    Grand_Total_Sale = Total_Sale
    Grand_Total_Profit_and_Lose = Grand_Total_Sale - Grand_Total_Purchase - Grand_Total_Expense

    html_string = render_to_string('pdfs/manufacture_purchase_report.html', {
        'results': results,
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        'user': request.user,
        'date': datetime.now().strftime('%d/%m/%Y'),
        'Grand_Total_Expense': "%.2f" % Grand_Total_Expense,
        'Grand_Total_Purchase': "%.2f" % Grand_Total_Purchase,
        'Grand_Total_Sale': "%.2f" % Grand_Total_Sale,
        'Grand_Total_Profit_and_Lose': "%.2f" % Grand_Total_Profit_and_Lose
    })

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ManufacturePurchaseReport.pdf"'
    return response
@login_required
def ClientProfile(request,pk):
    clientdata=Client.objects.get(user=request.user,Whats_App_Numbe=pk)
    print(pk)
    clientSale=Sale.objects.filter(user=request.user,Client_ID__Whats_App_Numbe=pk)
    saleReturn=Sale_Return.objects.filter(user=request.user,Client_ID__Whats_App_Numbe=pk)
    clientid=pk
    total_sale=0
    total_pending_payment=0
    total_paid_payment=0
    total_sale_Return=0
    for sales in saleReturn:
        total_sale_Return=sales.Return_To_Customer_Amount

     
    for data in clientSale:
        total_sale+=data.Final_Amount
        
        if data.Payment_Status==False:
            total_pending_payment+=data.Remaining
        
        total_paid_payment+=data.Paid_Amount



        
    print(clientSale)
    print(total_sale)
  
    if request.htmx:
        return render(request, 'components/Clientprofile.html',{'clientid':clientid,'clientdata': clientdata,'clientSale':clientSale,'total_sale':total_sale,'total_pending_payment':total_pending_payment,'total_paid_payment':total_paid_payment,'total_sale_Return':total_sale_Return})
    else:
      return render(request,"Clientprofile.html",{ 'clientid':clientid ,'clientdata': clientdata,'clientSale':clientSale,'total_sale':total_sale,'total_pending_payment':total_pending_payment,'total_paid_payment':total_paid_payment,'total_sale_Return':total_sale_Return})
@login_required
def SalewithClient(request):
    client_id = request.GET.get('Client_ID')
    item=request.GET.get('item')
    client = Client.objects.get(Whats_App_Number=client_id)
    
    check=False
    limit=client.Credit_Limit
    if limit==0.00:
        check=True
        
    saleproduct=Manufacturing.objects.filter(user=request.user,Out_Of_Stock=False)
    pending=Sale.objects.filter(user=request.user,Client_ID=client_id,Payment_Status=False)
    pendingTotal=Decimal(0.00)

    for pe in pending:
        pendingTotal+=pe.Remaining
     
    

    client_data = {
        'Full_Name': client.Full_Name,
        'WhatsApp': client.Whats_App_Number,
        'Phone_Number': client.Phone_Number,
        'Shiping_Address': client.Billing_Address,
        'Shipping_City': client.City,
        'Shiping_State': client.State,
        'Client_Credit':client.Credit_Limit
    }
    return render(request,"components/SaleForm.html",{'client_id':client_id,'client_data':client_data,'saleproduct': saleproduct,' pendingTotal': pendingTotal})
@login_required
def SaleGenerate(request):
    if request.method=="POST":

        Sale_Production_Name=request.POST.get("Sale_Production_Name")
        Items_Or_Balles=Decimal(request.POST.get("Items_Or_Balles"))
        Weight=request.POST.get("Weight")
        Weight_Unit=request.POST.get("Weight_Unit")
        Computer_Weight_Slip=request.FILES["Computer_Weight_Slip"]
        Sale_Price=request.POST.get("Sale_Price")
        Total_Amount=request.POST.get("Total_Amount")
        Client_Name=request.POST.get("Client_Name")
        Client_Phone_Number=request.POST.get("Client_Phone_Number")
        Client_ID=request.POST.get("Client_ID")
        Shiping_Address=request.POST.get("Shiping_Address")
        Shipping_City=request.POST.get("Shipping_City")
        Shiping_State=request.POST.get("Shiping_State")
        Driver_Name=request.POST.get("Driver_Name")
        Vehicle_Number=request.POST.get("Vehicle_Number")
        Driver_Contact=request.POST.get("Driver_Contact")
        Vehicle_Weight=request.POST.get("Vehicle_Weight")
        VECHCLE_WEIGHT_Unit=request.POST.get("VECHCLE_WEIGHT_Unit")
        Discount=Decimal(request.POST.get("Discount"))
        GSTtax=Decimal(request.POST.get("GST_Percentage"))
        Final_Amount=request.POST.get("Final_Amount")
        Remaining=request.POST.get("Remaning")
        Payment_Slip=request.FILES["paymentslip"]
        Paid=request.POST.get("pay")
        ProductionName=Manufacturing.objects.get(user=request.user,Manufacturing_Product_Name=Sale_Production_Name)
        data=Client.objects.filter(user=request.user)
        balles=ProductionName.Total_Production_Items
        if Items_Or_Balles>balles:
            messages.info(request,"Balles/Items are out of stock")
            return redirect("SaleGenerate")
        payment_value=False
        if Final_Amount==Paid:
            payment_value=True

        profile_instance= get_object_or_404(Profile, user=request.user)
        client_instance =get_object_or_404(Client, Whats_App_Number=Client_ID)
        client_instance.Credit_Limit-Decimal(Final_Amount)
        client_instance.save()
         
        
        query=Sale.objects.create(user=request.user,userprofile=profile_instance,Sale_Production_Name=Sale_Production_Name,Items_Or_Balles=Items_Or_Balles,Weight=Weight,Weight_Unit=Weight_Unit,Computer_Weight_Slip=Computer_Weight_Slip,Sale_Price=Sale_Price,Total_Amount=Total_Amount,Payment_Status=payment_value,Client_Name=Client_Name,Client_Phone_Number=Client_Phone_Number,Client_ID=client_instance,Shiping_Address=Shiping_Address,Shipping_City=Shipping_City,Shiping_State=Shiping_State,Driver_Name=Driver_Name,Vehicle_Number=Vehicle_Number,Driver_Contact=Driver_Contact,Vehicle_Weight=Vehicle_Weight,VECHCLE_WEIGHT_Unit=VECHCLE_WEIGHT_Unit,Final_Amount=Final_Amount,Discount=Discount,Paid_Amount=Paid,Remaining=Remaining,Payment_Slip=Payment_Slip,GST=GSTtax)
        query.save()
        items=Decimal(Items_Or_Balles)
        amount=Decimal(Total_Amount)
        total_weight=Decimal(Weight)

        updateManufactureSale=Manufacturing.objects.get(user=request.user,Manufacturing_Product_Name=Sale_Production_Name)
    
        updateManufactureSale.Total_Production_Items-=items
        updateManufactureSale.Total_Sale_Amount+=amount
        updateManufactureSale.Weight-=total_weight
        updateManufactureSale.save()
        if updateManufactureSale.Total_Production_Items<=0.00 or updateManufactureSale.Weight<=0.00 :
            updateManufactureSale.Out_Of_Stock=True
            Profit_and_Loses=updateManufactureSale.Total_Sale_Amount-updateManufactureSale.Total_Purchase_Price-updateManufactureSale.Manufacturing_Expense
            updateManufactureSale.Profit_OR_Lose=Profit_and_Loses
            updateManufactureSale.save()
            Profile.objects.filter(user=request.user).update(
            Total_Sale=F("Total_Sale")+Final_Amount,Balance=F("Balance")+Profit_and_Loses,Profit_OR_Lose=F("Profit_OR_Lose")+Profit_and_Loses
        )
        

        return redirect("currentInvoice",pk=Client_ID)
    data=Client.objects.filter(user=request.user)
    Products=Manufacturing.objects.filter(user=request.user,Out_Of_Stock=False).all()
    if request.htmx:
        return render(request, 'components/SaleGenerate.html',{'Products': Products,'data':data})
    else:
        return render(request,"VendorSale.html",{'Products': Products,'data':data })
@login_required
def client_search(request):
    query = request.GET.get('query', '')
    if query:
        clients = Client.objects.filter(user=request.user,Full_Name__icontains=query)
    else:
        clients = Client.objects.all()
    
    client_data = [{'Whats_App_Number': client.Whats_App_Number, 'Full_Name': client.Full_Name} for client in clients]
    return JsonResponse({'clients': client_data})

@login_required
def CurrentSale(request, pk):
    
    Invoice = Sale.objects.filter(user=request.user, Client_ID=pk).last()

    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Client_Name": Invoice.Client_Name,
        "Client_ID": Invoice.Client_ID,
        "client_address": Invoice.Shiping_Address,
        "client_city": Invoice.Shipping_City,
        "client_state": Invoice.Shiping_State,
        "client_mobile": Invoice.Client_Phone_Number,
        "Driver_Name": Invoice.Driver_Name,
        "Driver_Contact": Invoice.Driver_Contact,
        "Vehicle_number": Invoice.Vehicle_Number,
        "Vehicle_Weight": Invoice.Vehicle_Weight,
        "Vehicle_Weight_Unit": Invoice.VECHCLE_WEIGHT_Unit,
        "Paid_Amount": Invoice.Paid_Amount,
        "Remaining": Invoice.Remaining,
        "payment_status": "Paid" if Invoice.Payment_Status else "Pending",
        "Gst": Invoice.GST,
        "Items": Invoice.Items_Or_Balles,
        "Weight": Invoice.Weight,
        "Weight_Unit": Invoice.Weight_Unit,
        "Sale_Price": Invoice.Sale_Price,
        "Total_Amount": Invoice.Total_Amount,
        "Discount": Invoice.Discount,
        "Final_Amount": Invoice.Final_Amount,
        "invoice_number": f"{Invoice.Final_Amount}-{Invoice.id}",
        "user": request.user,
        "Sale_Production_Name":Invoice.Sale_Production_Name
    }

    html_string = render_to_string('pdfs/current_sale_invoice.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="SaleInvoice.pdf"'
    return response



@login_required
def currentInvoice(request, pk):
    
  
   
    client=Client.objects.filter(user=request.user,Whats_App_Number=pk).first()
    
     
    Invoice = Sale.objects.filter(user=request.user,Client_ID=client).last()
    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Client_Name": Invoice.Client_Name,
        "Client_ID": Invoice.Client_ID,
        "client_address": Invoice.Shiping_Address,
        "client_city": Invoice.Shipping_City,
        "client_state": Invoice.Shiping_State,
        "client_mobile": Invoice.Client_Phone_Number,
        "Driver_Name": Invoice.Driver_Name,
        "Driver_Contact": Invoice.Driver_Contact,
        "Vehicle_number": Invoice.Vehicle_Number,
        "Vehicle_Weight": Invoice.Vehicle_Weight,
        "Vehicle_Weight_Unit": Invoice.VECHCLE_WEIGHT_Unit,
        "Paid_Amount": Invoice.Paid_Amount,
        "Remaining": Invoice.Remaining,
        "payment_status": "Paid" if Invoice.Payment_Status else "Pending",
        "Gst": Invoice.GST,
        "Items": Invoice.Items_Or_Balles,
        "Weight": Invoice.Weight,
        "Weight_Unit": Invoice.Weight_Unit,
        "Sale_Price": Invoice.Sale_Price,
        "Total_Amount": Invoice.Total_Amount,
        "Discount": Invoice.Discount,
        "Final_Amount": Invoice.Final_Amount,
        "invoice_number": f"{Invoice.Final_Amount}-{Invoice.id}",
        "user": request.user,
        "Sale_Production_Name":Invoice.Sale_Production_Name
    }

    html_string = render_to_string('pdfs/current_sale_invoice.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="SaleInvoice.pdf"'
    return response
     

@login_required
def ClientSearchAndPurchase(request,pk):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = Sale.objects.filter(user=request.user,Client_ID=pk)
    customerid=pk
    
    if query:
        results = results.filter(Sale_Production_Name__icontains=query)
    if query2:
        results = results.filter(Vehicle_Number__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)    
      
    if request.htmx:
        return render(request,'components/ClientPurchaseSearch.html',{'customerid':customerid,'query':query,'query2':query2,'fromdate':fromdate,'todate':todate,'results':results} )
    else:
        return render(request,'ClientPurchaseSearch.html',{'customerid':customerid,'query':query,'query2':query2,'fromdate':fromdate,'todate':todate,'results':results} )
@login_required
def ClientReport(request, pk):
    query = request.GET.get('query')
    query2 = request.GET.get('query2')
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get('todate')

    client = Client.objects.filter(user=request.user, Whats_App_Numbe=pk).first()
    if not client:
        return HttpResponse("Client not found", status=404)

    results = Sale.objects.filter(user=request.user, Client_ID=client)
    if query:
        results = results.filter(Sale_Production_Name__icontains=query)
    if query2:
        results = results.filter(Vehicle_Number__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__gte=fromdate, date__lte=todate)

    

    Total_Purchase_Amount = sum(r.Total_Amount for r in results)
    Total_Paid_Amount = sum(r.Paid_Amount for r in results)
    Total_Pending_Amount = sum(r.Remaining for r in results)

    for sale in results:
        sale.PaymentStatusDisplay = "Paid" if sale.Payment_Status else "Pending"

    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        'user': request.user,
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Client_Name": client.Full_Name,
        "Client_ID": pk,
        "client_city": client.City,
        "client_mobile": client.Phone_Number,
        "client_state": client.State,
        "sales": results,
        "Total_Purchase_Amount": Total_Purchase_Amount,
        "Total_Paid_Amount": Total_Paid_Amount,
        "Total_Pending_Amount": Total_Pending_Amount,
        "request": request,  # to show authorized user name in template
    }

    html_string = render_to_string("pdfs/client_report.html", context)

    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="ClientReport_{pk}.pdf"'
    return response
@login_required
def Client_export_to_excel(request,pk):
    # Query the database
    data = Sale.objects.filter(user=request.user,Client_ID=pk).values()
    df = pd.DataFrame(list(data))
    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=clientReportExcel.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def SaleManagement(request):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = Sale.objects.filter(user=request.user)

    if query:
        results = results.filter(Client_Name__icontains=query)
    if query2:
        results = results.filter(Shiping_Address__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)    
      
    if request.htmx:
        return render(request,'components/SaleSearch.html',{'query':query,'query2':query2,'fromdate':fromdate,'todate':todate,'results':results} )
    else:
        return render(request,'SaleSearch.html',{'query':query,'query2':query2,'fromdate':fromdate,'todate':todate,'results':results} )
@login_required
def SaleReport(request):
    query = request.GET.get('query')
    query2 = request.GET.get('query2')
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get('todate')
    results = Sale.objects.filter(user=request.user)

    if query:
        results = results.filter(Client_Name__icontains=query)
    if query2:
        results = results.filter(Client_ID__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)

    

    context = {
         
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        'Date': datetime.now().strftime("%d/%m/%Y"),
        'sales': results,
        'Total_Purchase_Amount': sum(r.Total_Amount for r in results),
        'Total_Paid_Amount': sum(r.Paid_Amount for r in results),
        'Total_Pending_Amount': sum(r.Remaining for r in results),
    }

    html_string = render_to_string('pdfs/sale_report.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ClientSaleReport.pdf"'
    return response
@login_required
def VendorSale_export_to_excel(request):
    # Query the database
    data = Sale.objects.filter(user=request.user,).values()
    df = pd.DataFrame(list(data))
    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=VendorSale.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def paymentIn(request, pk, id):
    if request.method == "POST":
        Pay_Amount = Decimal(request.POST.get('Pay_Amount'))
        Remaining_Payment = Decimal(request.POST.get('Remaining_Amount'))
        
        try:
            Pay_Amount = float(Pay_Amount)
            Remaining_Payment = float(Remaining_Payment)
        except (ValueError, TypeError):
            # Handle the error or provide feedback to the user
            return render(request, 'paymentIn.html', {
                'pk': pk, 'id': id, 'error': 'Invalid payment amounts provided.'
            })
        
        query = Sale.objects.filter(
            user=request.user,
            Client_ID=pk,
            id=id,
            Payment_Status=False
        ).update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining=F('Remaining') - Pay_Amount
        )
        
        if Remaining_Payment == 0:
            Sale.objects.filter(
                user=request.user,
                Client_ID=pk,
                id=id,
                Payment_Status=False
            ).update(Payment_Status=True)
        url = reverse('currentPaymentInPdf', kwargs={'pk': pk, 'id': id})
        return redirect(url)    
    client_PaymentIn = Sale.objects.get(
        user=request.user,
        Client_ID=pk,
        id=id,
        Payment_Status=False
    )
    
    pending = client_PaymentIn.Remaining
    
    template = 'components/paymentIn.html' if request.htmx else 'paymentIn.html'
    return render(request, template, {
        'pk': pk,
        'id': id,
        'client_PaymentIn': client_PaymentIn,
        'pending': pending
    })
 
@login_required
def Itemchecking(request):
    items = request.POST.get('Sale_Production_Name')
    
    balles = int(request.POST.get('Items_Or_Balles'))  # Convert to integer
 
     
    item = Manufacturing.objects.get(Manufacturing_Product_Name=items)
    it = int(item.Total_Production_Items)
    
    if it < balles:
        print("working")
        return JsonResponse({'exists': True})
    
    return JsonResponse({'exists': False})
@login_required
def currentPaymentInPdf(request,pk,id):
    customerid=pk
    return render(request,'PaymentInPDF.html',{'customerid':customerid,'id':id})
@login_required
def paymentInSlip(request, pk,id):
    Invoice = Sale.objects.get(user=request.user, Client_ID=pk,id=id)
    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Client_Name": Invoice.Client_Name,
        "Client_ID": Invoice.Client_ID,
        "client_address": Invoice.Shiping_Address,
        "client_city": Invoice.Shipping_City,
        "client_state": Invoice.Shiping_State,
        "client_mobile": Invoice.Client_Phone_Number,
        "Driver_Name": Invoice.Driver_Name,
        "Driver_Contact": Invoice.Driver_Contact,
        "Vehicle_number": Invoice.Vehicle_Number,
        "Vehicle_Weight": Invoice.Vehicle_Weight,
        "Vehicle_Weight_Unit": Invoice.VECHCLE_WEIGHT_Unit,
        "Paid_Amount": Invoice.Paid_Amount,
        "Remaining": Invoice.Remaining,
        "payment_status": "Paid" if Invoice.Payment_Status else "Pending",
        "Gst": Invoice.GST,
        "Items": Invoice.Items_Or_Balles,
        "Weight": Invoice.Weight,
        "Weight_Unit": Invoice.Weight_Unit,
        "Sale_Price": Invoice.Sale_Price,
        "Total_Amount": Invoice.Total_Amount,
        "Discount": Invoice.Discount,
        "Final_Amount": Invoice.Final_Amount,
        "invoice_number": f"{Invoice.Final_Amount}-{Invoice.id}",
        "user": request.user,
    }

    html_string = render_to_string('pdfs/current_sale_invoice.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="SaleInvoice.pdf"'
    return response
@login_required
def add_expense(request):
    compydetail = CompanyDetail.objects.first()
    balance = Profile.objects.get(user=request.user)
    productions = Manufacturing.objects.filter(user=request.user, Complete_Production=False)
    totalBalance = balance.Balance

    if request.method == 'POST':
        production_name = request.POST.get('name')
        if not production_name:
            messages.warning(request, "Please Select Bunkar Name")
            return redirect("add_expense")

        category = request.POST.get('category')
        if not category:
            messages.warning(request, "Please Select Expense Category")
            return redirect("add_expense")

        harvesting_type = request.POST.get('harvesting-type')

        amount = Decimal(request.POST.get('amount') or '0.0')
        payment_status = request.POST.get('payment_status')
        if not payment_status:
            messages.warning(request, "Please Select Payment Status")
            return redirect("add_expense")

        if payment_status == "PAID":
            Paid_amount = amount
            Remaining = Decimal('0.0')
        else:
            Paid_amount = Decimal(request.POST.get('paid_amount') or '0.0')
            Remaining = amount - Paid_amount

        # Additional fields
        description = request.POST.get('description')
        fuel_price = Decimal(request.POST.get('fuel-price') or '0.0')
        total_fuel = Decimal(request.POST.get('total-fuel') or '0.0')
        total_acre = Decimal(request.POST.get('total-acre') or '0.0')
        price_per_acre = Decimal(request.POST.get('harvest-price-per-acre') or '0.0')
        notes = request.POST.get('notes')
        bill = request.FILES.get('expensebill')

        profile_instance = get_object_or_404(Profile, user=request.user)
        manufacture_qs = Manufacturing.objects.filter(user=request.user, Manufacturing_Product_Name=production_name)

        # Handle Harvesting special cases
        if category == "Harvesting":
            if harvesting_type == "Fuel":
                manufacture_qs.update(
                    Harvesting_Cost=F("Harvesting_Cost") + amount,
                    Manufacturing_Expense=F("Manufacturing_Expense") + amount,
                    Harvest_Type=harvesting_type,
                    Total_Fuel=F("Total_Fuel") + total_fuel,
                    Fuel_Price=F("Fuel_Price") + fuel_price
                )
            elif harvesting_type == "Without Fuel":
                if not total_acre or not price_per_acre:
                    messages.warning(request, "Fill all fields for Harvesting Without Fuel")
                    return redirect("HarvestingExpense")
                manufacture_qs.update(
                    Harvesting_Cost=F("Harvesting_Cost") + amount,
                    Manufacturing_Expense=F("Manufacturing_Expense") + amount,
                    Harvest_Type=harvesting_type,
                    Total_Harvest_Acer=F("Total_Harvest_Acer") + total_acre,
                    Harvest_Acer_Cost=F("Harvest_Acer_Cost") + price_per_acre
                )

        # Update Manufacturing based on category
        category_updates = {
            "Pressing": "Pressing_Cost",
            "Dumping": "Dumping_Cost",
            "Polythene": "Polythene_Cost",
            "Mud Cost": "Mud_Cost",
            "Balling Paper": "Packing_Material",
            "Stitch Paper": "Packing_Material",
            "Machine Depreciation": "Machine_Depreciation",
            "Loading": "Loading_Cost",
            "Labour": "Labour_Expense"
        }

        cost_field = category_updates.get(category, "Other_Expense")

        manufacture_qs.update(**{
            cost_field: F(cost_field) + amount,
            "Manufacturing_Expense": F("Manufacturing_Expense") + amount
        })

        # Save Expense
        Expense.objects.create(
            user=request.user,
            userprofile=profile_instance,
            Production_Name=production_name,
            description=description,
            category=category,
            amount=amount,
            Bill_Proof=bill,
            notes=notes,
            Payment_Status=payment_status,
            Paid_Amount=Paid_amount,
            Remaining_Amount=Remaining
        )

        # Update Profile total
        Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense") + amount
        )

        messages.success(request, "Expense Added Successfully. Download Your Expense Bill PDF")
        return redirect('expensebill')

    template = 'components/expense_form.html' if request.htmx else 'expense_form.html'
    return render(request, template, {
        'totalBalance': totalBalance,
        'productions': productions,
        'compydetail': compydetail
    })

@login_required
def expenseManagement(request):
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get('todate')

    # Start with an empty filter set
    results = Expense.objects.filter(user=request.user)

    # Apply date filters if provided
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)

    # Apply pagination after filtering
    paginator = Paginator(results, 8)  # Show 3 expenses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'fromdate': fromdate,
        'todate': todate,
        'results': page_obj,  # Pass paginated results
        'page_obj': page_obj,  # Pass the page object for pagination controls
    }

    # Render appropriate template based on whether HTMX is used
    if request.htmx:
        return render(request, 'components/expensemanagement.html', context)
    else:
        return render(request, 'expensemanagement.html', context)
@login_required
def expensebill(request):
    return render(request,"expensebill.html") 
@login_required
def generate_expense_report(request):
    
    expenses = Expense.objects.filter(user=request.user).order_by('date')
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get("todate")

    if fromdate and todate:
        expenses = expenses.filter(date__gte=fromdate, date__lte=todate)

   
     

    total_amount = sum(exp.amount for exp in expenses)
    total_paid = sum(exp.Paid_Amount or 0 for exp in expenses)
    total_remaining = sum(exp.Remaining_Amount or 0 for exp in expenses)
    

    context = {
        'company_name': request.user.company_name,
        'company_email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'total_amount': total_amount,
        'total_paid': total_paid,
        'total_remaining': total_remaining,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        'date': datetime.now().strftime("%d/%m/%Y"),
        'expenses': expenses,
        'total_amount': total_amount,
        'fromdate': fromdate,
        'todate': todate,
    }

    # Render HTML template
    html_string = render_to_string('pdfs/expense_report.html', context)

    # Generate PDF
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ExpenseReport.pdf"'
    return response
@login_required
def ExpenseSlip(request):
    # Get the latest expense for this user
    expense = Expense.objects.filter(user=request.user).last()

    # Context for the template
    context = {
        'company_name': request.user.company_name,
        'company_email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        'date': datetime.now().strftime("%d/%m/%Y"),
        'expense': expense,
    }

    # Render the HTML template to a string
    html_string = render_to_string('pdfs/expensebillslip.html', context)

    # Generate PDF
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    # Return response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ExpenseReport.pdf"'
    return response

@login_required
def expense_Excel(request):
    # Query the database
    data = Expense.objects.filter(user=request.user).values()
    df = pd.DataFrame(list(data))

    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=expenseReport.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def VendorPayementOut(request):
    balance=Profile.objects.get(user=request.user)
    totalBalance=balance.Balance
    print(totalBalance)
    if totalBalance==0.00:
        messages.warning(request,"You Have Low Balance")
    
    if request.method == 'POST':
        name=request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        amount =Decimal(request.POST.get('amount'))
        bill = request.FILES['expensebill']
        notes = request.POST.get('notes')
        profile_instance= get_object_or_404(Profile, user=request.user)
        query=PaymentOut.objects.create(user=request.user,userprofile=profile_instance,name=name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes)
        query.save()
        balance=Profile.objects.filter(user=request.user).update(
            Balance=F("Balance")-amount
        )
        if totalBalance==0.00:
            messages.warning(request,"You Have Low Balance")
            return render("VendorPaymentOut")

        
        # Redirect to a success page or do further processing
        return redirect('withdrwalSlip')  # Replace with your success URL or view name
    if request.htmx:
        return render(request,'components/PaymentOut.html',{'totalBalance':totalBalance})
    else:
        return render(request, 'PaymentOut.html',{'totalBalance':totalBalance})
@login_required
def PaymentOutSlip(request):
    # Fetch the last expense record for the user
    expenses = PaymentOut.objects.filter(user=request.user).last()

    # Set up the response and PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PaymentOutSlip.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)
    
    # Fetch company details (assuming there's only one company)
    try:
        company_detail = CompanyDetail.objects.filter(user=request.user).first()
    except CompanyDetail.DoesNotExist:
        company_detail = None

    # Default values if no company details found
    if company_detail:
        company_name = company_detail.name
        company_email = company_detail.email
        head_office = company_detail.Head_Office
        phone_number = company_detail.phone
        company_logo_path = company_detail.logo  # Adjust with actual attribute name for logo URL
    else:
        company_name = "Your Company Name"
        company_email = "company@example.com"
        head_office = "1234 Main St, Anytown, AN"
        phone_number = "(123) 456-7890"
        company_logo_path = "media/default_logo.png"  # Replace with default logo path

    date = datetime.now().strftime("%d/%m/%Y")

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    paragraph_style = styles['Normal']
    footer_style = ParagraphStyle('footer', fontSize=10, alignment=1, textColor=colors.grey)

    # Create report content
    content = []

    # Company logo and details
    if company_logo_path:
        try:
            company_logo = Image(company_logo_path, width=100, height=100)
        except Exception as e:
            print(f"Failed to load company logo: {str(e)}")
            company_logo = None
    else:
        company_logo = None

    if company_logo:
        content.append(company_logo)
    
    content.append(Paragraph(company_name, title_style))
    content.append(Paragraph(head_office, paragraph_style))
    content.append(Paragraph(phone_number, paragraph_style))
    content.append(Paragraph(company_email, paragraph_style))
    content.append(Spacer(1, 20))

    # Report title and summary
    content.append(Paragraph("Payment Withdrawal Slip", heading_style))
    content.append(Paragraph("Report Date: {}".format(date), paragraph_style))
    content.append(Spacer(1, 20))

    # Expenses table
    data = [
        ["Name", "Category", "Amount", "Date"]
    ]
     
    if expenses:
        data.append([expenses.name, expenses.category, "{:.2f}".format(expenses.amount), expenses.date.strftime("%d/%m/%Y")])
    else:
        data.append(["N/A", "N/A", "N/A", "N/A"])

    col_widths = [150, 100, 100, 100]  # Adjust column widths
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ])
    
    expenses_table = Table(data, colWidths=col_widths)
    expenses_table.setStyle(table_style)
    content.append(expenses_table)
    content.append(Spacer(1, 20))

    # Footer
    content.append(Paragraph("", footer_style))

    # Build the PDF document
    pdf.build(content)
    return response
@login_required
def withdrwalSlip(request):
    return render(request,"WithdrwalSlip.html")
@login_required
def transactionHistory(request):
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = PaymentOut.objects.filter(user=request.user)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)    
      
    if request.htmx:
        return render(request,'components/TransactionHistory.html',{'fromdate':fromdate,'todate':todate,'results':results})
    else:
        return render(request, 'TransactionHistory.html',{'fromdate':fromdate,'todate':todate,'results':results})
@login_required
def generate_Transactions_report(request):
    # Fetch data from the database
    results  = PaymentOut.objects.filter(user=request.user)
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)   
    # Calculate totals
    total_amount = Decimal(0.00)
    for expense in results:
        total_amount += expense.amount

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="TranscationHistory.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    
    # Fetch company details (assuming there's only one company)
    try:
        company_detail = CompanyDetail.objects.filter(user=request.user).first()
    except CompanyDetail.DoesNotExist:
        company_detail = None

    # Default values if no company details found
    if company_detail:
        company_name = company_detail.name
        company_email = company_detail.email
        head_office = company_detail.Head_Office
        phone_number = company_detail.phone
        company_logo_path = company_detail.logo  # Adjust with actual attribute name for logo URL
    else:
        company_name = "Your Company Name"
        company_email = "company@example.com"
        head_office = "1234 Main St, Anytown, AN"
        phone_number = "(123) 456-7890"
        company_logo_path = "media/default_logo.png"  # Replace with default logo path

    date = datetime.now().strftime("%d/%m/%Y")

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    paragraph_style = styles['Normal']
    footer_style = ParagraphStyle('footer', fontSize=10, alignment=1, textColor=colors.grey)

    # Create report content
    content = []

    # Company logo and details
    if company_logo_path:
        try:
            company_logo = Image(company_logo_path, width=100, height=100)
        except Exception as e:
            print(f"Failed to load company logo: {str(e)}")
            company_logo = None
    else:
        company_logo = None

    if company_logo:
        content.append(company_logo)
    
    content.append(Paragraph(company_name, title_style))
    content.append(Paragraph(head_office, paragraph_style))
    content.append(Paragraph(phone_number, paragraph_style))
    content.append(Paragraph(company_email, paragraph_style))
    content.append(Spacer(1, 20))

    # Report title and summary
    content.append(Paragraph("Transaction History " , heading_style))
    content.append(Paragraph("Report Date: {}".format(date), paragraph_style))
    content.append(Spacer(1, 20))

    # Expenses table
    data = [
        ["Name","Category", "Amount", "Date"]
    ]
    for expns in results:
        data.append([expns.name,expns.category, "{:.2f}".format(expns.amount), expns.date.strftime("%d/%m/%Y")])

    col_widths = [200,150, 100, 100]  # Adjust column widths
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
    ])
    
    expenses_table = Table(data, colWidths=col_widths)
    expenses_table.setStyle(table_style)
    content.append(expenses_table)
    content.append(Spacer(1, 20))

    # Summary table
    summary = [
        ["Total Amount", "{:.2f}".format(total_amount)]
    ]
    summary_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    summary_table = Table(summary, colWidths=[150, 100])
    summary_table.setStyle(summary_table_style)
    content.append(summary_table)
    content.append(Spacer(1, 20))

    # Footer
    content.append(Paragraph("", footer_style))

    # Build the PDF document
    pdf.build(content)
    return response
@login_required
def Transaction_export_to_excel(request):
    # Query the database
    data = PaymentOut.objects.filter(user=request.user).values()
    df = pd.DataFrame(list(data))

    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=TranscationReport_data.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def Salereturn(request):
    productions=Manufacturing.objects.filter(user=request.user)
    clients=Client.objects.filter(user=request.user)
    if request.method=="POST":
        Product=request.POST.get('Sale_Production_Name')
        Client_ID=request.POST.get('Client_ID')
        client_instance =Client.objects.get(user=request.user, Whats_App_Number=Client_ID)
        client_Name=client_instance.Full_Name
        item= request.POST.get('Items_Or_Balles')
        weight = request.POST.get('Weight')
        amount =Decimal(request.POST.get('Return_To_Customer_Amount'))
        bill = request.FILES['Payment_Proof']
        reason = request.POST.get('Reason_Of_Return')
        profile_instance= get_object_or_404(Profile, user=request.user)
        Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=Product).update(
            Weight=F("Weight")+weight,Total_Production_Items=F("Total_Production_Items")+item,Total_Sale_Amount=F("Total_Sale_Amount")-amount,Profit_OR_Lose=F("Profit_OR_Lose")-amount,Out_Of_Stock=False
        )
        Sale.objects.filter(user=request.user,Sale_Production_Name=Product,Client_ID=Client_ID).update(
         Weight=F("Weight")+weight,Items_Or_Balles=F("Items_Or_Balles")+item,Final_Amount=F("Final_Amount")-amount  
        )
        query=Sale_Return.objects.create(user=request.user,userprofile=profile_instance,Client_ID=client_instance,Client_Name=client_Name,Sale_Production_Name=Product,Items_Or_Balles=item,Weight=weight,Return_To_Customer_Amount=amount,Payment_Proof=bill,Reason_Of_Return=reason)
        query.save()
        messages.success(request,"Sale Return Record Added!")
        return redirect("Vendor")
    if request.htmx:
        return render(request,"components/SaleReturn.html",{'clients':clients,'productions':productions})
    else:
        return render(request,"SaleReturn.html",{'clients':clients,'productions':productions})
@login_required
def SaleReturnManagement(request):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = Sale_Return.objects.filter(user=request.user)

    if query:
        results = results.filter(Client_Name__icontains=query)
    if query2:
        results = results.filter(Client_ID__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)    
      
    if request.htmx:
        return render(request,'components/SaleReturnmanagement.html',{'query':query,'query2':query2,'fromdate':fromdate,'todate':todate,'results':results} )
    else:
        return render(request,'SaleReturnmanagement.html',{'query':query,'query2':query2,'fromdate':fromdate,'todate':todate,'results':results} )
@login_required
def SaleReturnReport(request):
    query = request.GET.get('query')
    query2 = request.GET.get('query2')
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get("todate")

    results = Sale_Return.objects.filter(user=request.user)
    if query:
        results = results.filter(Client_Name__icontains=query)
    if query2:
        results = results.filter(Client_ID__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)

    compydetail = CompanyDetail.objects.filter(user=request.user).first()
    Total_Return_Amount = sum(r.Return_To_Customer_Amount for r in results)

    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Total_Return_Amount": Total_Return_Amount,
        "sale_returns": results,
        "user": request.user,
    }

    html_string = render_to_string('pdfs/sale_return_report.html', context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="SaleReturnReport.pdf"'
    return response
@login_required
def VendorSaleReturn_export_to_excel(request):
    # Query the database
    data = Sale_Return.objects.filter(user=request.user,).values()
    df = pd.DataFrame(list(data))
    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=VendorSale.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def generate_daily_report(request):
    today = date.today()
    
    # Fetch company details
    try:
        company_detail = CompanyDetail.objects.filter(user=request.user).first()
    except CompanyDetail.DoesNotExist:
        company_detail = None

    if company_detail:
        company_name = company_detail.name
        company_email = company_detail.email
        head_office = company_detail.Head_Office
        phone_number = company_detail.phone
        company_logo_path = os.path.join(settings.MEDIA_ROOT, str(company_detail.logo))  # Adjust with actual attribute name for logo URL
    else:
        company_name = "Your Company Name"
        company_email = "company@example.com"
        head_office = "1234 Main St, Anytown, AN"
        phone_number = "(123) 456-7890"
        company_logo_path = os.path.join(settings.MEDIA_ROOT, "default_logo.png")  # Replace with default logo path

    profiles = Profile.objects.all()

    for pro in profiles:
        total_sales = Sale.objects.filter(date=today, user=pro.user).aggregate(total=models.Sum('Final_Amount'))['total'] or 0
        total_production = DailyProduction.objects.filter(date=today, user=pro.user).aggregate(total=models.Sum('Total_Production_Item'))['total'] or 0
        total_expenses = Expense.objects.filter(date=today, user=pro.user).aggregate(total=models.Sum('amount'))['total'] or 0
        total_payment_out = PaymentOut.objects.filter(date=today, user=pro.user).aggregate(total=models.Sum('amount'))['total'] or 0

        # Create PDF report
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        heading_style = styles['Heading1']
        paragraph_style = styles['Normal']
        footer_style = ParagraphStyle('footer', fontSize=10, alignment=1, textColor=colors.grey)

        content = []

        # Company logo and details
        if company_logo_path:
            try:
                company_logo = Image(company_logo_path, width=100, height=100)
            except Exception as e:
                print(f"Failed to load company logo: {str(e)}")
                company_logo = None
        else:
            company_logo = None

        if company_logo:
            content.append(company_logo)

        content.append(Paragraph(company_name, title_style))
        content.append(Paragraph(head_office, paragraph_style))
        content.append(Paragraph(phone_number, paragraph_style))
        content.append(Paragraph(company_email, paragraph_style))
        content.append(Spacer(1, 20))

        # Report title and summary
        content.append(Paragraph("Daily Report", heading_style))
        content.append(Paragraph(f"Report Date: {today}", paragraph_style))
        content.append(Spacer(1, 20))

        # Report details
        data = [
            ["Total Sales", "Total Production", "Total Expenses", "Total Payment Out", "Remaining Balance"]
        ]
        data.append([
            f"{total_sales:.2f}",
            f"{total_production:.2f}",
            f"{total_expenses:.2f}",
            f"{total_payment_out:.2f}",
            f"{pro.Balance:.2f}"  # Assuming `Balance` is a field in Profile
        ])

        col_widths = [100, 100, 100, 100, 100]  # Adjust column widths
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ])

        report_table = Table(data, colWidths=col_widths)
        report_table.setStyle(table_style)
        content.append(report_table)
        content.append(Spacer(1, 20))

        # Footer
        content.append(Paragraph("", footer_style))

        # Build the PDF document
        pdf.build(content)
        buffer.seek(0)

        # Send email with PDF attachment
        email = EmailMessage(
            'Daily Report',
            'Please find attached the daily report.',
            settings.DEFAULT_FROM_EMAIL,
            ['shoaib0033237@gmail.com'],  # Send to each user's email
        )
        email.attach(f'{pro.user}_daily_report_{today}.pdf', buffer.read(), 'application/pdf')
        email.send()

@login_required
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_daily_report, 'interval', hour=0,minute=0,second=0)  # Adjust time as needed
    scheduler.start()
@login_required
def search(request):
    # Retrieve search text from the POST request
    search_text = request.POST.get('search')
    # Filter categories based on name containing search text
    results2 = Client.objects.filter(user=request.user,Full_Name__icontains=search_text)
    print(results2)
    # Prepare context to pass to the template
    context = {'results2': results2}
    # Render search result template with context
    return render(request, 'components/searchresult.html', context)
@login_required
def FraudDector(request):
    mail=Profile.objects.get(user=request.user)
    alert=mail.email

    subject = f'Fraud Have Been Detected From Admin'
    message = (
        f'Dear {request.user}. The Record Of Your Sales Have Been Change By The Admin Please Take Action To Resolve the Issues\n\n'
         
    )
    send_mail(subject, message,  settings.EMAIL_HOST_USER, [alert])
     
 
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Manufacturing, Profile
@login_required
def AddManufecturePurchase(request):
    if request.method == "POST":
        Purchase_Type = request.POST.get("Purchase_Type")
        Location = request.POST.get("Production_Place")
        supplier = request.POST.get("sname")
        BunkarName = request.POST.get("Product_Name")
        Acers = request.POST.get("total_acer")
        acer_purchase_price = request.POST.get("acer_purchase_price")
        total_amount_acers_str = request.POST.get("total_amount_acers")
        Total_Weight = request.POST.get("Total_Weight")
        Purchase_Weight_Price = request.POST.get("Purchase_Weight_Price")
        Total_Amount_Weight_str = request.POST.get("Wtotal")
        paymentMethod = request.POST.get("paymentMethod")

        # Set Paid_amount and Remaining to "0" if empty
        Paid_amount = request.POST.get("Paid_amount", "0")
        Remaining = request.POST.get("Remaining", "0")

        profile_instance = get_object_or_404(Profile, user=request.user)
        value = False
        if paymentMethod == "Paid":
            value = True  # Fixed assignment issue

        # Check for duplicate entry based on Manufacturing_Product_Name
        if Manufacturing.objects.filter(Manufacturing_Product_Name=BunkarName).exists():
            messages.warning(request, 'Bunkar Name Already Exists, Please Enter Unique Bunkar Name')
            return redirect('AddManufecturePurchase')

        # Validate and convert total_amount_acers to Decimal
        try:
            total_amount_acers = Decimal(total_amount_acers_str) if total_amount_acers_str else Decimal(0)
        except InvalidOperation:
            messages.error(request, "Invalid amount format for total_amount_acers.")
            return redirect('AddManufecturePurchase')

        # Validate and convert Total_Amount_Weight to Decimal
        try:
            Total_Amount_Weight = Decimal(Total_Amount_Weight_str) if Total_Amount_Weight_str else Decimal(0)
        except InvalidOperation:
            messages.error(request, "Invalid amount format for Total_Amount_Weight.")
            return redirect('AddManufecturePurchase')

        # Convert Paid_amount and Remaining to Decimal with validation
        try:
            Paid_amount = Decimal(Paid_amount) if Paid_amount else Decimal(0)
        except InvalidOperation:
            messages.error(request, "Invalid amount format for Paid Amount.")
            return redirect('AddManufecturePurchase')

        try:
            Remaining = Decimal(Remaining) if Remaining else Decimal(0)
        except InvalidOperation:
            messages.error(request, "Invalid amount format for Remaining Amount.")
            return redirect('AddManufecturePurchase')

        if Purchase_Type == "PER_ACER":
            if total_amount_acers <= 0:
                messages.info(request, "Please Fill All Calculation Fields")
                return redirect("AddManufecturePurchase")

            Manufacturing.objects.create(
                user=request.user,
                userprofile=profile_instance,
                Manufacturing_Product_Name=BunkarName,
                Manufacturing_Purchase_Type=Purchase_Type,
                Supplier_Name=supplier,
                Place_Of_Supply=Location,
                Total_Acers=Acers,
                Per_Acer_Purchase_Price=acer_purchase_price,
                Total_Purchase_Price=total_amount_acers,
                Paid_Amount=Paid_amount,
                Remaining_Amount=Remaining,
                Payment_Status=value
            )
            messages.info(request, "Bunkar Record Added! Please Add Expense Of Your New Bunkar")
            return redirect("add_expense")

        if Purchase_Type == "PURCHASE_WEIGHT":
            if Total_Amount_Weight <= 0:
                messages.info(request, "Please Fill All Calculation Fields")
                return redirect("AddManufecturePurchase")

            Manufacturing.objects.create(
                user=request.user,
                userprofile=profile_instance,
                Manufacturing_Product_Name=BunkarName,
                Manufacturing_Purchase_Type=Purchase_Type,
                Supplier_Name=supplier,
                Place_Of_Supply=Location,
                Weight=Total_Weight,
                Manufacture_Weight=Total_Weight,
                Purchase_Weight_Price=Purchase_Weight_Price,
                Total_Purchase_Price=Total_Amount_Weight,
                Paid_Amount=Paid_amount,
                Remaining_Amount=Remaining,
                Payment_Status=value
            )
            messages.info(request, "Bunkar Record Added! Please Add Expense Of Your New Bunkar")
            return redirect("add_expense")

    if request.htmx:
        return render(request, "components/Purchaseform.html")
    else:
        return render(request, 'ManufacturePurchaseForm.html')
@login_required
def HarvestingExpense(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Harvesting.html",{'productions':productions})
    else:
        return render(request,'Harvesting.html',{'productions':productions})
@login_required
def Dumping(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Dumping.html",{'productions':productions})
    else:
        return render(request,'Dumping.html',{'productions':productions})
@login_required
def Polythene(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Polythene.html",{'productions':productions})
    else:
        return render(request,'Polythene.html',{'productions':productions})
@login_required
def PackingMaterial(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Packing.html",{'productions':productions})
    else:
        return render(request,'Packing.html',{'productions':productions})
@login_required
def WeightLose(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.method == 'POST':
        production_name=request.POST.get('name')
        weightlosevalue = request.POST.get('weightlosevalue')
        manufaccture_instance=Manufacturing.objects.get(user=request.user,Manufacturing_Product_Name=production_name)
        original_weight2 = manufaccture_instance.Manufacture_Weight # Assume this is a Decimal field
        print(original_weight2)
        weightlose_percentage = Decimal(weightlosevalue) / 100
        print(weightlose_percentage)
        deduction2 = original_weight2 *  weightlose_percentage # Calculate 3% deduction
        new_weight2 = original_weight2 - deduction2
        manufaccture_instance.Manufacture_Weight = new_weight2
        manufaccture_instance.save()
        manufaccture_instance.Weight_Losses=weightlosevalue
        manufaccture_instance.save()
        print(new_weight2)# Save the updated instance
        return redirect("Vendor")
    if request.htmx:
        return render(request,"components/WeightLose.html",{'productions':productions})
    else:
          return render(request,'WeightLose.html',{'productions':productions})
         
     
  
@login_required
def add_production_labour(request):
    if request.method == 'POST':
        team_leader = request.POST.get('team_leader')
        profile_instance = Profile.objects.get(user=request.user)
        # Create and save a new Production_Labour instance
        Production_Labour.objects.create(
            userprofile=profile_instance,
            user=request.user,
            Team_Leader=team_leader,
        )
        messages.success(request, "Production Labour data added successfully!")
        return redirect('AddDailyProduction')  # Redirect to a list view or another view
    if request.htmx:
        return render(request,"components/add_production_labour.html")
    else:
        return render(request, 'add_production_labour.html')
   

@login_required
def add_loading_labour(request):
    if request.method == 'POST':
        team_leader = request.POST.get('team_leader')
        profile_instance = Profile.objects.get(user=request.user)
       

        # Create and save a new Loading_Labour instance
        Loading_Labour.objects.create(
            userprofile=profile_instance,
            user=request.user,
            Team_Leader=team_leader,
        )
        
        messages.success(request, "Loading Labour data added successfully!")
        return redirect('add_expense')  # Redirect to a list view or another view
    if request.htmx:
        return render(request,"components/add_loading_labour.html")
    else:
        return render(request, 'add_loading_labour.html')

    

 
@login_required
def add_loading_labour_record(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    labour=Loading_Labour.objects.filter(user=request.user)
    if request.method == 'POST':
        
        team_leader = request.POST.get('team_leader')
        

        bankar = request.POST.get('name')
        bales = request.POST.get('bales')
        per_bale_price = request.POST.get('per_bale_price')
        payment_status = request.POST.get('payment_status')
        total_amount=request.POST.get('total_amount')
        paid_amount=request.POST.get('paid_amount')
        remaining=request.POST.get('remaining')
        if not paid_amount:  # Check if the value is empty or None
            paid_amount = Decimal('0.0')
        else:
            paid_amount = Decimal(paid_amount)
        # Handling Remaining Amount
         
        if not remaining:  # Check if the value is empty or None
            remaining = Decimal('0.0')
        else:
            remaining = Decimal(remaining)
        account=Loading_Labour.objects.get(user=request.user,id=team_leader)
        update=Loading_Labour.objects.filter(user=request.user,id=team_leader)
        profile_instance = Profile.objects.get(user=request.user)
        productions = Manufacturing.objects.filter(user=request.user, Complete_Production=False)
        manufaccture_instance=Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=bankar)
        manufaccture_instance.update(Pressing_Cost=F("Loading_Cost")+total_amount,Manufacturing_Expense=F("Manufacturing_Expense")+total_amount)
        
        Profile.objects.filter(user=request.user).update(
        Total_Expense=F("Total_Expense")+total_amount)
        if payment_status=="CREDIT":
             update.update(Credit=F("Credit")+remaining,Paid=F("Paid")+paid_amount,Bales=F("Bales")+bales)
        else:
             update.update(Paid=F("Paid")+ total_amount,Bales=F("Bales")+bales)
        # Create and save a new LoadingLabourRecord instance
        LoadingLabourRecord.objects.create(
            user=request.user,
            userprofile=profile_instance,
            Team_Leader=account.Team_Leader,
            Bankar=bankar,
            Bales=bales,
            Per_Bale_Price=per_bale_price,
            Total_Amount=total_amount,
            Paid_Amount=paid_amount,
            Remaining=remaining,
            Payment_Status=payment_status,
            Labour_Id=team_leader
        )
        
        messages.success(request, "Loading Labour Record data added successfully!")
        return redirect('Vendor')  # Redirect to a list view or another view

    return render(request, 'add_loading_labour_record.html',{'productions':productions,'labour':labour})
@login_required
def search1(request):
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = ProducctionLabourRecord.objects.filter(user=request.user)
    count=ProducctionLabourRecord.objects.filter(user=request.user).count()
    

    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)
        messages.info(request,f"{count} Record Found In Production Labour")    
      
    if request.htmx:
        return render(request,'components/ProductionLabourRecord.html',{'fromdate':fromdate,'todate':todate,'results':results})
    else:
        return render(request, 'ProductionLabourRecord.html',{'fromdate':fromdate,'todate':todate,'results':results})
@login_required
def generate_Production_Labour_report(request):
    results = ProducctionLabourRecord.objects.filter(user=request.user)
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get('todate')
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)
     
 
    total_amount = sum([record.Total_Amount for record in results])
    paid=sum([record.Paid_Amount for record in results])
    pending=sum([record.Remaining for record in results])

     

    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "date": datetime.now().strftime("%d/%m/%Y"),
        "records": results,
        "total_amount": total_amount,
        "paid":paid,
        "pending":pending
    }

    html_string = render_to_string("pdfs/production_labour_report.html", context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=ProductionLabourReport.pdf"
    return response
@login_required
def Production_Labour_Excel(request):
    # Query the database
    data = ProducctionLabourRecord.objects.filter(user=request.user).values()
    df = pd.DataFrame(list(data))

    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ProductionLabour.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def search2(request):
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results =  LoadingLabourRecord.objects.filter(user=request.user)
    count= LoadingLabourRecord.objects.filter(user=request.user).count()
    

    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)
        messages.info(request,f"{count} Record Found In Loading Labour")    
      
    if request.htmx:
        return render(request,'components/LoadingLabourRecord.html',{'fromdate':fromdate,'todate':todate,'results':results})
    else:
        return render(request, 'LoadingLabourRecord.html',{'fromdate':fromdate,'todate':todate,'results':results})
@login_required
def generate_Loading_Labour_report(request):
    results2 = LoadingLabourRecord.objects.filter(user=request.user)
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get('todate')
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)
     
 
    total_amount = sum([record.Total_Amount for record in results2])
    paid=sum([record.Paid_Amount for record in results2])
    pending=sum([record.Remaining for record in results2])

     

    context = {
        'company_name': request.user.company_name,
        'email': request.user.email,
        'head_office': request.user.business_address,
        'phone_number': request.user.phone_number,
        'prepared_by':request.user.first_name,
        'company_logo_path': request.build_absolute_uri(request.user.business_logo.url) if request.user.business_logo else '',
        "date": datetime.now().strftime("%d/%m/%Y"),
        "records": results2,
        "key_for_loading":True,
        "total_amount": total_amount,
        "paid":paid,
        "pending":pending,
        
    }

    html_string = render_to_string("pdfs/production_labour_report.html", context)
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=ProductionLabourReport.pdf"
    return response
@login_required
def Loading_Labour_Excel(request):
    # Query the database
    data = LoadingLabourRecord.objects.filter(user=request.user).values()
    df = pd.DataFrame(list(data))

    # Create an Excel writer using Pandas
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=LoadingLabour.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
@login_required
def CreditToPaid(request, id):
    if request.method == "POST":
        Labour_id=request.POST.get('Labour_id')
        
        Pay_Amount = Decimal(request.POST.get('Pay_Amount'))
        Remaining_Payment = Decimal(request.POST.get('Remaining_Amount'))
        Pending_Amount = Decimal(request.POST.get('Pending_Amount'))
        
        try:
            Pay_Amount = float(Pay_Amount)
            Remaining_Payment = float(Remaining_Payment)
        except (ValueError, TypeError):
            # Handle the error or provide feedback to the user
            return render(request, ' CreditToPaid.html', {
                  'id': id, 'error': 'Invalid payment amounts provided.'
            })
        
        ProducctionLabourRecord.objects.filter(
        user=request.user,
        pk=id,
        Payment_Status="CREDIT"
        ).update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining=F('Remaining') - Pay_Amount,
            Credit=F("Credit")-Pay_Amount

            
        )
        Expense.objects.filter(user=request.user,Remaining_Amount=Pending_Amount,Payment_Status="CREDIT").update(
        Paid_Amount=F('Paid_Amount') + Pay_Amount,
        Remaining_Amount=F('Remaining_Amount') - Pay_Amount,

        )  
        
        if Remaining_Payment == 0:
            ProducctionLabourRecord.objects.filter(
                user=request.user,
                pk=id,
                Payment_Status="CREDIT"
            ).update(Payment_Status="PAID")
            Expense.objects.filter(user=request.user,Remaining_Amount=Pending_Amount).update(
            Payment_Status="PAID"
        )
            Expense.objects.filter(user=request.user,Remaining_Amount=Pending_Amount,Payment_Status="CREDIT").update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining_Amount=F('Remaining_Amount') - Pay_Amount
             

        )
         
        labour=Production_Labour.objects.get(user=request.user,pk=Labour_id)
        if labour.Advance>0:
            if Pay_Amount<=labour.Advance:
                Production_Labour.objects.filter(user=request.user,pk=Labour_id).update(
                Advance=F('Advance') -Pay_Amount,
                Paid=F('Paid') + Pay_Amount,
                Credit=F('Credit') - Pay_Amount)
            else:
              Production_Labour.objects.filter(user=request.user,pk=Labour_id).update(
              Paid=F('Paid') + Pay_Amount,
              Credit=F('Credit') - Pay_Amount

        )
        else:
            Production_Labour.objects.filter(user=request.user,pk=Labour_id).update(
            Paid=F('Paid') + Pay_Amount,
            Credit=F('Credit') - Pay_Amount

        )
        
        

       
        messages.info(request,"Bill Have Been Paid To Production Labour ")
        return redirect("Vendor")  
       
    Paymentout = ProducctionLabourRecord.objects.get(
        user=request.user,
        pk=id,
        Payment_Status="CREDIT"

    )
    
    
    template = 'components/CreditToPaid.html' if request.htmx else 'CreditToPaid.html'
    return render(request, template, {
        'id': id,
        'data':Paymentout,
         
    })
@login_required
def CreditToPaidLoading(request, id):
    if request.method == "POST":
        Labour_id = request.POST.get('Labour_id')
        print(Labour_id)
        Pay_Amount = Decimal(request.POST.get('Pay_Amount'))
        Remaining_Payment = Decimal(request.POST.get('Remaining_Amount'))
        Pending_Amount = Decimal(request.POST.get('Pending_Amount'))
        
        try:
            Pay_Amount = float(Pay_Amount)
            Remaining_Payment = float(Remaining_Payment)
        except (ValueError, TypeError):
            # Handle the error or provide feedback to the user
            return render(request, ' CreditToPaidLoading.html', {
                  'id': id, 'error': 'Invalid payment amounts provided.'
            })
        
        LoadingLabourRecord.objects.filter(
        user=request.user,
        pk=id,
        Payment_Status="CREDIT"
        ).update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining=F('Remaining') - Pay_Amount,
            Credit=F("Credit")-Pay_Amount

            
        )
        Expense.objects.filter(user=request.user,Remaining_Amount=Pending_Amount,Payment_Status="CREDIT").update(
        Paid_Amount=F('Paid_Amount') + Pay_Amount,
        Remaining_Amount=F('Remaining_Amount') - Pay_Amount,

        )  
        
        if Remaining_Payment == 0:
            LoadingLabourRecord.objects.filter(
                user=request.user,
                pk=id,
                Payment_Status="CREDIT"
            ).update(Payment_Status="PAID")
            Expense.objects.filter(user=request.user,Remaining_Amount=Pending_Amount).update(
            Payment_Status="PAID"
        )
            Expense.objects.filter(user=request.user,Remaining_Amount=Pending_Amount,Payment_Status="CREDIT").update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining_Amount=F('Remaining_Amount') - Pay_Amount
             

        )
        labour=Loading_Labour.objects.get(user=request.user,pk=Labour_id)
        if labour.Advance>0:
            if Pay_Amount<=labour.Advance:
                Loading_Labour.objects.filter(user=request.user,pk=Labour_id).update(
                Advance=F('Advance') -Pay_Amount,
                Paid=F('Paid') + Pay_Amount,
                Credit=F('Credit') - Pay_Amount)
            else:
              Loading_Labour.objects.filter(user=request.user,pk=Labour_id).update(
              Paid=F('Paid') + Pay_Amount,
              Credit=F('Credit') - Pay_Amount

        )
        else:
            Loading_Labour.objects.filter(user=request.user,pk=Labour_id).update(
            Paid=F('Paid') + Pay_Amount,
            Credit=F('Credit') - Pay_Amount

        )
        
        

   
        
       
        messages.info(request,"Bill Have Been Paid To Loading Labour ")
        return redirect("Vendor")  
       
    Paymentout = LoadingLabourRecord.objects.get(
        user=request.user,
        pk=id,
        Payment_Status="CREDIT"

    )
    
     
    
    
    
    
    template = 'components/CreditToPaidLoading.html' if request.htmx else 'CreditToPaidLoading.html'
    return render(request, template, {
        'id': id,
        'data':Paymentout,
         
    })
@login_required
def BunkarExpense(request, id):
    if request.method == "POST":
        Pay_Amount = Decimal(request.POST.get('Pay_Amount'))
        Remaining_Payment = Decimal(request.POST.get('Remaining_Amount'))
        
        try:
            Pay_Amount = float(Pay_Amount)
            Remaining_Payment = float(Remaining_Payment)
        except (ValueError, TypeError):
            # Handle the error or provide feedback to the user
            return render(request, ' CreditToPaidLoading.html', {
                  'id': id, 'error': 'Invalid payment amounts provided.'
            })
        
        Expense.objects.filter(
        user=request.user,
        pk=id,
        Payment_Status="CREDIT"
        ).update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining_Amount=F('Remaining_Amount') - Pay_Amount,
            

            
        )
         
        if Remaining_Payment == 0:
            Expense.objects.filter(
                user=request.user,
                pk=id,
                Payment_Status="CREDIT"
            ).update(Payment_Status="PAID")

       
        messages.info(request,"Bill Have Been!!! ")
        return redirect("Vendor")  
       
    Paymentout = Expense.objects.get(
        user=request.user,
        pk=id,
        Payment_Status="CREDIT"

    )

    
    
     
    
    
    
    
    template = 'components/Bunkarexpense.html' if request.htmx else 'Bunkarexpense.html'
    return render(request, template, {
        'id': id,
        'data':Paymentout,
         
    })
 
 

@login_required
def fetch_details(request, bunkar):
    # Fetch the details based on the selected name from the database
    purchase = Manufacturing.objects.get(user=request.user,Manufacturing_Product_Name=bunkar)
    
    # Send back the required fields as JSON
    print(purchase.Weight,purchase.Manufacturing_Purchase_Type)
    data = {
        'total_expense': purchase.Manufacturing_Expense,
        'purchase_price': purchase.Total_Purchase_Price,
        'purchase_type': purchase.Manufacturing_Purchase_Type,
        'total_weight': purchase.Weight  
    }
    
    return JsonResponse(data)
@login_required
def Estimater(request):
    if request.method=="POST":
        bunkar=request.POST.get("bunkar")
        purchase_type=request.POST.get("purchase_type")
        weight_lose=request.POST.get("weight_loss_percentage")
        calculated_weight_value=request.POST.get("calculated_weight_value")
        remaining_weight=request.POST.get("remaining_weight")
        per_kg_price=request.POST.get("per_kg_price")
        if purchase_type=="PER_ACER":
            Manufacturing.objects.filter(Manufacturing_Product_Name=bunkar).update(
                Weight=F("Weight")+calculated_weight_value,Manufacture_Weight=F("Manufacture_Weight")+calculated_weight_value,
                Estimated_weight=F("Estimated_weight")+calculated_weight_value, Weight_After_Weight_Lose=F("Weight_After_Weight_Lose")+remaining_weight,Weight_Lose_Value=F("Weight_Lose_Value")+weight_lose,
                Per_Kg_Or_Mund_Price=F("Per_Kg_Or_Mund_Price")+ per_kg_price
            )
            messages.info(request,"Bunkar with Estimated Record Added!!")
            return redirect("Vendor")
        else:
            Manufacturing.objects.filter(Manufacturing_Product_Name=bunkar).update(
                Weight_After_Weight_Lose=F("Weight_After_Weight_Lose")+remaining_weight,Weight_Lose_Value=F("Weight_Lose_Value")+weight_lose,
                Per_Kg_Or_Mund_Price=F("Per_Kg_Or_Mund_Price")+ per_kg_price
            )
            messages.info(request,"Bunkar with Estimated Record Added!!")
            return redirect("Vendor")
    else:
        return redirect("Vendor")

@login_required
def Loading_Labour_Advance(request):
    labour=Loading_Labour.objects.filter(user=request.user)
    if request.method == "POST":
        Labour_Id =  request.POST.get('Labour_id') 
        Payment = Decimal(request.POST.get('payment'))
        Team=Loading_Labour.objects.get(pk=Labour_Id)
        Team_Leader=Team.Team_Leader
        query= Loading_Labour_Advance_Payment.objects.create(
            user=request.user,
            Team_Leader=Team_Leader,
            Advance=Payment 

        )
        query.save()
        Loading_Labour.objects.filter(pk=Labour_Id).update(
            Advance=F("Advance")+Payment
        )
        messages.info(request,"Advance Payment Added For Production Labour ")
        return redirect("Vendor")

    
    if request.htmx:
        return render(request,'components/Advance_payment.html',{'labour':labour} )
    else:
        return render(request, 'Advance_payment.html',{'labour':labour})
@login_required
def Production_Labour_Advance(request):
    labour=Production_Labour.objects.filter(user=request.user)
    if request.method == "POST":
        Labour_Id =  request.POST.get('Labour_id') 
        Payment = Decimal(request.POST.get('payment'))
        Team=Production_Labour.objects.get(pk=Labour_Id)
        Team_Leader=Team.Team_Leader
        query=Production_Labour_Advance_Payment.objects.create(
            user=request.user,
            Team_Leader=Team_Leader,
            Advance=Payment 

        )
        query.save()
        Production_Labour.objects.filter(pk=Labour_Id).update(
            Advance=F("Advance")+Payment
        )
        messages.info(request,"Advance Payment Added For Production Labour ")
        return redirect("Vendor")

    
    if request.htmx:
        return render(request,'components/Production_Labour_Payments.html',{'labour':labour} )
    else:
        return render(request, 'Production_Labour_Payments.html',{'labour':labour})

  # Replace with your actual model

def CustomerSearch(request):
    query = request.GET.get('query')
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get('todate')
    results = Sale.objects.filter(Client_ID=query)
    
     

    if fromdate and todate and not query:
        messages.warning(request, "Please enter your Customer ID.")
    else:
        if query:
            results = Sale.objects.filter(Client_ID=query)

        if fromdate and todate:
            results = Sale.objects.filter(Client_ID=query,date__lte=todate, date__gte=fromdate)
   
    return render(request, 'Customer.html', {
        'query': query,
        'fromdate': fromdate,
        'todate': todate,
        'results': results,
    })

def  CustomerSaleReport(request):
    query = request.GET.get('query')
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get('todate')
    results = Sale.objects.filter(Client_ID=query)

    if fromdate and todate and not query:
        messages.warning(request, "Please enter your Customer ID.")
    else:
        if query:
            results = Sale.objects.filter(Client_ID=query)

        if fromdate and todate:
            results = Sale.objects.filter(Client_ID=query,date__lte=todate, date__gte=fromdate)
      
    compydetail = CompanyDetail.objects.all()    
    
    
    comN = []
    Email = []
    address = []
    phone = []
    for com in compydetail:
        name = com.name
        comN.append(name)
        email = com.email
        Email.append(email)
        office = com.Head_Office
        address.append(office)
        Phone = com.phone
        phone.append(Phone)
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ClientReport.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Define data for the invoice
    compydetail = CompanyDetail.objects.filter(user=request.user).first()
    company_logo_path = compydetail.logo
    company_name = compydetail.name
    company_email = compydetail.email
    Head_Office = compydetail.Head_Office
    Phone = compydetail.phone 
    Date = datetime.now().strftime("%d/%m/%Y")
    Total_Purchase_Amount=0
    Total_Pending_Amount=0
    Total_Paid_Amount=0
    
    for salereport in results: 
        Total_Purchase_Amount+=salereport.Total_Amount
        Total_Paid_Amount+=salereport.Paid_Amount
        Total_Pending_Amount+=salereport.Remaining


         
         
    
    sale = [
        ["Client","Items/Balles", "Weight",  "Sale Price", "Total Amount", "Discount", "Final Amount","Pay Amount","Status"],]
    for report in results:
        paymentstatus="Pending"
      
        if report.Payment_Status==True:
           paymentstatus="Paid"
       
          
           
        sale.append([str(report.Client_Name),str(report.Items_Or_Balles), str(report.Weight),  str(report.Sale_Price), str(report.Total_Amount), str(report.Discount), str(report.Final_Amount),str(report.Paid_Amount),str(paymentstatus)]
    )
    

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    paragraph_style = styles['Normal']

    # Define table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Create invoice content
    content = []

    # Company details and logo
    company_logo = Image(company_logo_path, width=90, height=90)

    # Header and Company Details
    header_data = [
        [company_logo, Paragraph("<b>{}</b>".format(company_name), title_style)],
        ["", Paragraph("{}".format(company_email), paragraph_style)],
        ["", Paragraph("{}".format(Head_Office), paragraph_style)],
        ["", Paragraph("{}".format(Phone), paragraph_style)],
    ]

    header_table = Table(header_data, colWidths=[100, 400])
    content.append(header_table)
    content.append(Spacer(1, 12))
    invoice_number = random.randint(100000, 999999)
    # Client and Driver details in parallel
    client_driver_details = [
        ["Report Number",str(invoice_number), "Date", Date,],
        ["Customer ID",  str(query), "Total Purchase Amount", str(Total_Purchase_Amount)], 
        ["Total Paid Amount", str(Total_Paid_Amount), "Total Pending",  str(Total_Pending_Amount)],
       
        
    ]

    details_data = [[Paragraph("<b>{}</b>".format(detail[0]), paragraph_style), Paragraph(detail[1], paragraph_style),
                     Paragraph("<b>{}</b>".format(detail[2]), paragraph_style), Paragraph(detail[3], paragraph_style)] for detail in client_driver_details]
    details_table = Table(details_data, colWidths=[220, 150, 150, 150])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    content.append(details_table)
    content.append(Spacer(1, 12))

    # Sale items table
    items_table = Table(sale, colWidths=[70, 60, 90, 80, 80, 70, 80, 70])
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
@login_required
def ManufactureCredit(request,bunkar):
    if request.method == "POST":
        
        Pay_Amount = Decimal(request.POST.get('Pay_Amount'))
        Remaining_Payment = Decimal(request.POST.get('Remaining_Amount'))

        Paid = Manufacturing.objects.get(
        user=request.user,
        Manufacturing_Product_Name=bunkar,
        Payment_Status=False

    )
        
        try:
            Pay_Amount = float(Pay_Amount)
            Remaining_Payment = float(Remaining_Payment)
        except (ValueError, TypeError):
            # Handle the error or provide feedback to the user
            return render(request, ' CreditToPaid.html', {
                  'id': id, 'error': 'Invalid payment amounts provided.'
            })
        Pay=float(Paid.Remaining_Amount)
        if Pay-Pay_Amount==0:
           Manufacturing.objects.filter(
           Manufacturing_Product_Name=bunkar,
         ).update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining_Amount=F('Remaining_Amount') - Pay_Amount,
            Payment_Status=True

        )
        else:
           Manufacturing.objects.filter(
           Manufacturing_Product_Name=bunkar,
        ).update(
            Paid_Amount=F('Paid_Amount') + Pay_Amount,
            Remaining_Amount=F('Remaining_Amount') - Pay_Amount,
        

        )

    
        
    
       
        
        
        
          
        
        

       
        messages.info(request,"Bill Have Been Paid To Supplier ")
        return redirect("Vendor")  
       
    Paymentout = Manufacturing.objects.get(
        user=request.user,
        Manufacturing_Product_Name=bunkar,
        Payment_Status=False

    )
    
    
    template = 'components/ManufactureCredit.html' if request.htmx else 'ManufactureCredit.html'
    return render(request, template, {
        'id': id,
        'data':Paymentout,
         
    })


def Invocing(request):
    return render(request,"Invoice.html")

 
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import CustomUserSignupForm
from django.conf import settings
from django.core.files.storage import default_storage


@require_http_methods(["POST"])
def send_otp_view(request):
    form = CustomUserSignupForm(request.POST, request.FILES)

    if form.is_valid():
        data = {
            'username': form.cleaned_data['username'],
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'email': form.cleaned_data['email'],
            'phone_number': form.cleaned_data['phone_number'],
            'company_name': form.cleaned_data['company_name'],
            'license_no': form.cleaned_data['license_no'],
            'password1': form.cleaned_data['password1'],
            'password2': form.cleaned_data['password2'],
        }

        # Save files temporarily and store paths (optional)
        if 'business_logo' in request.FILES:
            path = default_storage.save(f"temp/business_logo_{data['username']}.jpg", request.FILES['business_logo'])
            data['business_logo_path'] = path

        if 'document' in request.FILES:
            path = default_storage.save(f"temp/document_{data['username']}.pdf", request.FILES['document'])
            data['document_path'] = path

        request.session['signup_data'] = data

        # Generate and send OTP via email
        otp = generate_otp()
        cache_key = f"otp_email_{data['email']}"
        cache.set(cache_key, otp, timeout=300)  # 5 minutes
        print(otp)
        # Send email (simplified)
        # send_mail(
        #     subject="Your OTP Code",
        #     message=f"Your OTP code is: {otp}",
        #     from_email="noreply@yourdomain.com",
        #     recipient_list=[data['email']],
        # )

        return JsonResponse({
            'success': True,
            'message': 'OTP sent successfully',
            'email': data['email']
        })

    return JsonResponse({
        'success': False,
        'errors': form.errors
    }, status=400)
@require_http_methods(["POST"])
def resend_otp_view(request):
    signup_data = request.session.get('signup_data')

    if not signup_data:
        return JsonResponse({"success": False, "message": "Session expired. Please start again."})

    phone_number = signup_data['phone_number']
    otp = generate_otp()
    cache.set(f"otp_{phone_number}", otp, timeout=300)

    # send_mail(
    #     'Your Resent OTP for Vendor Signup',
    #     f'Your new OTP is {otp}',
    #     settings.DEFAULT_FROM_EMAIL,
    #     [signup_data['email']],
    #     fail_silently=False,
    # )

    return JsonResponse({"success": True, "message": "OTP resent successfully"})
def signup_view(request):
    return render(request,"signupform.html")
@require_POST
def signup_api_view(request):
    from random import randint

    form = CustomUserSignupForm(request.POST,request.FILES)
    
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        request.session['signup_email'] = user.email

        otp = str(randint(100000, 999999))
        OTPRecord.objects.create(user=user, otp_code=otp)

        # send_mail(
        #     subject='Your OTP Code',
        #     message=f'Your OTP code is: {otp}',
        #     from_email='evergreencornsilageservice@gmail.com',
        #     recipient_list=[user.email],
        #     fail_silently=True
        # )
        print(otp)

        return JsonResponse({
            'success': True,
            'message': f'OTP sent to {user.email}',
            'email': user.email
        })
    else:
        errors = form.errors.get_json_data()
        return JsonResponse({
            'success': False,
            'errors': errors,
            'message': 'There were errors with your form submission.'
        }, status=400)


def generate_otp():
    """Generate 6-digit OTP"""
    return str(random.randint(100000, 999999))




 

@require_http_methods(["POST", "GET"])
def verify_email_otp_view(request):
    """Verify OTP sent to user's email (no signup logic)."""
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if not entered_otp:
            return JsonResponse({"success": False, "message": "OTP is required."}, status=400)

        check_otp = OTPRecord.objects.filter(otp_code=entered_otp).first()
        print("CHECK OTP:", check_otp)

        if check_otp is None:
            return JsonResponse({"success": False, "message": "Invalid OTP code."}, status=400)

        if check_otp.is_used:
            return JsonResponse({"success": False, "message": "OTP has already been used."}, status=400)

        if check_otp.otp_code == entered_otp:
            check_otp.is_used = True
            check_otp.save()

            user = User.objects.filter(email=check_otp.user.email).first()
            if user:
                user.is_active = True
                user.save()

            return JsonResponse({"success": True, "message": "Account Created!"}, status=200)
        else:
            return JsonResponse({"success": False, "message": "Invalid OTP."}, status=400)

    else:
        return render(request, 'verify_email_otp.html')

def checkemail(request):
    email=request.POST.get('email')
    if User.objects.filter(email=email).exists():
        return JsonResponse({'status': 'email_exists'})
    else:
        return JsonResponse({'status': 'email_not_exists'})
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse


def get_access_token():
    url = f"{settings.BSECURE_API_BASE_URL}/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": f"{settings.BSECURE_CLIENT_ID}:{settings.BSECURE_STORE_ID}",
        "client_secret": settings.BSECURE_CLIENT_SECRET
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("body", {}).get("access_token")
    return None

def initiate_payment(request):
    access_token = get_access_token()
    if not access_token:
        return JsonResponse({"success": False, "message": "Failed to get access token"})

    # Order Payload
    order_payload = {
        "store_id": settings.BSECURE_STORE_ID,
        "lang": "en",
        "order_id": "ORDER1234334423334347",
        "total_amount": 1000,
        "sub_total_amount": 1000,
        "discount_amount": 0,
        "shipment_charges": 150,
        "shipment_method_name": "Standard",
        "products": [
            {
                "id": "prod90",
                "name": "Test Product",
                "sku": "TP-001",
                "quantity": 1,
                "price": 1000,
                "discount": 0,
                "sale_price": 1000,
                "sub_total": 1000,
                "image": "https://yourdomain.com/product.jpg"
            }
        ],
        "customer": {
            "name": "Test User",
            "email": "test@example.com",
            "country_code": "92",
            "phone_number": "3001234567"
        },
        "customer_address": {
            "country": "PK",
            "province": "Sindh",
            "city": "Karachi",
            "area": "Clifton",
            "address": "Test Address"
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"{settings.BSECURE_API_BASE_URL}/order/create"
    response = requests.post(url, json=order_payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        redirect_url = data.get("body", {}).get("checkout_url")  # Correct key

        if redirect_url:
            return redirect(redirect_url)
        else:
            return JsonResponse({
                "success": False,
                "message": "No checkout_url returned",
                "bsecure_response": data
            }, status=400)
    else:
        return JsonResponse({
            "success": False,
            "message": "Payment creation failed",
            "status_code": response.status_code,
            "response_text": response.text
        }, status=500)



def order_form(request):
    return render(request, "initiate_payment.html")

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from safepay_python.safepay import *

def get_or_create_event_loop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

# Setup Safepay Environment
env = Safepay(
    {
        "environment": "sandbox",
        "apiKey": "sec_edf830e8-8160-4427-b5a7-6d64e1610577",
        "v1Secret": "33c34303433bac9c02a1de7bce45492ebd2adc4bde2cad1c291cc958df494853",
        "webhookSecret": "foo",
    }
)
@login_required
def start_payment(request,plan_id):
    get_or_create_event_loop()
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    payment_response = env.set_payment_details({
        "currency": "PKR",
        "amount": plan.price   
    })

    token = payment_response["data"]["token"]
    sub, _ = UserSubscription.objects.get_or_create(user=request.user)
    sub.plan = plan
    sub.transaction_token = token
    sub.is_active = False
    sub.save()

    # Create checkout URL
    checkout_url = env.get_checkout_url({
        "beacon": token,
        "cancelUrl": request.build_absolute_uri(reverse("payment_cancel")),
        "orderId": "T80089",
        "redirectUrl": request.build_absolute_uri(reverse("payment_success")),
        "source": "custom",
        "webhooks": True,
    })

    return redirect(checkout_url)

@login_required
def payment_success(request):
    token = request.GET.get('tracker')
    sig = request.GET.get('order_id')

    sub = get_object_or_404(UserSubscription, transaction_token=token)
    sub.activate()
    

    if token:
        return render(request, "success.html",{"sub":sub})
    else:
        return render(request, "payment_failed.html")

@login_required
def payment_cancel(request):
    return render(request, "payment_cancel.html")


@csrf_exempt
def safepay_webhook(request):
    if request.method == "POST":
        signature = request.headers.get("x-sfpy-signature")
        data = request.body  # raw payload

        try:
            import json
            parsed_data = json.loads(data)

            valid = env.is_webhook_valid(
                {"x-sfpy-signature": signature},
                {"data": parsed_data}
            )

            if valid:
                # Mark invoice as paid
                return JsonResponse({"message": "Payment confirmed"}, status=200)
            else:
                return JsonResponse({"error": "Invalid signature"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.htmx:
        return render(request, 'components/profile.html',{"profile":profile})
    else:

      return render(request,"profile.html",{"profile":profile})
@require_http_methods(["GET", "POST"])
def password_reset_request_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect('password_reset_request')

        otp = str(random.randint(100000, 999999))
        OTPRecord.objects.create(user=user, otp_code=otp)

        # 
        print(otp)

        request.session['reset_email'] = email
        messages.success(request, "OTP sent to your email.")
        return redirect('password_reset_verify')

    return render(request, 'reset_request.html')


@require_http_methods(["GET", "POST"])
def password_reset_verify_view(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        email = request.session.get('reset_email')
        user = User.objects.get(email=email)
        otp_record = OTPRecord.objects.filter(user=user, otp_code=entered_otp, is_used=False).first()

        if otp_record:
            otp_record.is_used = True
            otp_record.save()
            request.session['otp_verified'] = True
            return redirect('password_reset_new_password')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('password_reset_verify')

    return render(request, 'reset_verify.html')


@require_http_methods(["GET", "POST"])
def password_reset_new_password_view(request):
    if not request.session.get('otp_verified'):
        return redirect('password_reset_request')

    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('password_reset_new_password')

        email = request.session.get('reset_email')
        user = User.objects.get(email=email)
        user.set_password(password1)
        user.save()

        messages.success(request, "Password reset successfully!")
        return redirect('login')

    return render(request, 'reset_new_password.html')
from django.contrib.auth import authenticate, login
from django.db.models import Q
def farm_vendor_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')  # this can be username OR email
        password = request.POST.get('password')

        # Try to find user by username OR email
        try:
            user = User.objects.get(Q(username=identifier) | Q(email=identifier),is_active=True)
        except User.DoesNotExist:
            user = None

        if user:
            # Authenticate using username (always)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Vendor')  # or your dashboard URL name
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            messages.error(request, 'Account not found. Please check your username/email.')
    
    return render(request, 'login.html')
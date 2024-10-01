from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from datetime import datetime,timedelta
from django.db.models import F
from django.db.models import Sum
from django.template.loader import render_to_string,get_template
import os
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.urls import reverse
import random
from datetime import date
from reportlab.pdfgen import canvas
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
from reportlab.lib.utils import ImageReader
def index(request):
    compydetail=CompanyDetail.objects.all()
    return render(request,"index.html", {'compydetail':compydetail})
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

def Vendor(request):
    current_year = datetime.now().year
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
    
    
                                
                       
    fetch=Manufacturing.objects.filter(user=request.user)
    pending=Sale.objects.filter(user=request.user)
    paymentRecived=Sale.objects.filter(user=request.user)
    total_purchase = Decimal(0.00)
    total_sale=Decimal(0.00)
    total_pending = Decimal(0.00)
    total_sales=Decimal(0.00)
    total_Recived_Payment=Decimal(0.00)
    siteexp=Decimal(0.00)
    manufacture_expense=Decimal(0.00)
    profit=Decimal(0.00)
    siteProfit=Decimal(0.00)
    withdraw=PaymentOut.objects.filter(user=request.user)
    for wd in withdraw:
        siteexp+=wd.amount or Decimal(0.00)




    for obj in fetch:
        total_purchase += obj.Total_Purchase_Price or Decimal(0.00)
        total_sale += obj.Total_Sale_Amount or Decimal(0.00)
        manufacture_expense += obj.Manufacturing_Expense or Decimal(0.00)
        profit +=total_sale- total_purchase-manufacture_expense
        

    for pen in pending:
        total_pending+=pen.Remaining
        total_sales+=pen.Final_Amount

    for pay in paymentRecived:
        total_Recived_Payment+=pay.Paid_Amount
    
    print(total_sale,total_sales)
    if total_sale<total_sales:
        messages.warning(request,"Fraud Have Been Detected From Admin")
        FraudDector(request)
    siteProfit=profit-siteexp
    context={
        'total_purchase':total_purchase,
        'total_sale':total_sale,
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
        
        
    }
    

   
    if request.htmx:
        return render(request, 'components/Vendor.html',context)
    else:

      return render(request,"Vendor.html",context)
    
def Addclient(request):
    compydetail=CompanyDetail.objects.all()
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
        query=Client.objects.create(user=request.user,userprofile=profile_instance,Full_Name=name,Email=email,Whats_App_Number=whatsappno,Phone_Number=phoneno,Billing_Address=address,City=city,State=state,Business_Name=bname,Acccount_Type=accountType,Opening_Balance=openingBalance,Credit_Limit=creditlimit,profilepic=clientPic)
        query.save()
        return redirect("SaleGenerate")
    if request.htmx:
        return render(request, 'components/AddClient.html',{'compydetail': compydetail})
    else:
        return render(request,"client.html",{'compydetail': compydetail})
     

   
     
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
            Payment_Status=payment_status
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
 
def Client_Whatsapp_filter(request):
    Client_Whatsapp=request.POST.get('WhatsAppNo')
    if Client.objects.filter(Whats_App_Number= Client_Whatsapp).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
def Client_mobileno_filter(request):
    Mobile=request.POST.get('mnumber')
    if Client.objects.filter(Whats_App_Number=Mobile).exists():
       return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
def check_product_name(request):
    product_name = request.GET.get('Product_Name', None)
    if product_name:
        exists = Manufacturing.objects.filter(Manufacturing_Product_Name=product_name).exists()
        print(exists)
        return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})
 


def NewPurchasepdf(request):
    if not request.user.is_authenticated:
        return HttpResponse("You need to log in to view this page.", status=401)
    compydetail=CompanyDetail.objects.all()
    purchase=DailyProduction.objects.filter(user=request.user).last()
    comN=[]
    Email=[]
    address=[]
    phone=[]
    for com in compydetail:
        name=com.name
        comN.append(name)
        email=com.email
        Email.append(email)
        office=com.Head_Office
        address.append(office)
        Phone=com.phone
        phone.append(Phone)




    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="productionInvoice.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define data for the invoice
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
    Head_Office = address[0]
    Phone = phone[0]
     
    Date= datetime.now().strftime("%d/%m/%Y")
    ProductionCity = purchase.City
    ProductionPlace= purchase.Production_Place
    
    items = [
        ["Puroduction","Items/Balles","Team" ,"Expense", "Date"],
        [purchase.Puroduction_Product_Name,purchase.Total_Production_Item,purchase.Production_Team_Name,  purchase.Total_Expense_Amount,purchase.date]
    ]

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    paragraph_style = styles['Normal']

    # Define table style
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create invoice content
    content = []

    # Company details and logo
    company_logo = Image(company_logo_path, width=100, height=100)
    content.append(company_logo)
    content.append(Paragraph(company_name, title_style))
    content.append(Paragraph("{}".format(Head_Office), paragraph_style))
    content.append(Paragraph(" {}".format(Phone), paragraph_style))
    content.append(Paragraph("{}".format(company_email), paragraph_style))
     

    # Client details
    content.append(Paragraph("____________________________________________", heading_style))
    content.append(Paragraph("Daily Production Record ", heading_style))
    content.append(Paragraph("Created Date: {}".format(Date), paragraph_style))
    content.append(Paragraph("Production City: {}".format(ProductionCity), paragraph_style))
    content.append(Paragraph("Production Place: {}".format(ProductionPlace), paragraph_style))
    content.append(Paragraph("", heading_style))

    # Invoice items table
    items_table = Table(items, colWidths=[200, 80, 80, 80])
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
# Create your views here.
def TotalVendorPurchase(request):
    compydetail=CompanyDetail.objects.all()
    purchase=DailyProduction.objects.filter(user=request.user)
    Total_Point_Production=DailyProduction.objects.filter(user=request.user).count()
    Expense_Amount=Decimal(0.00)
    Grand_Total=Decimal(0.00)
    for purchases in purchase:
        Expense_Amount+=purchases.Total_Expense_Amount
    Grand_Total=Expense_Amount
    print(Grand_Total)

        
    comN=[]
    Email=[]
    address=[]
    phone=[]
    for com in compydetail:
        name=com.name
        comN.append(name)
        email=com.email
        Email.append(email)
        office=com.Head_Office
        address.append(office)
        Phone=com.phone
        phone.append(Phone)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ProductionBill.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define data for the invoice
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
     
    Head_Office = address[0]
    Phone = phone[0]
     
    Date= datetime.now().strftime("%d/%m/%Y")
    Total_Amount= Grand_Total
    vendor_total_Production=Total_Point_Production
    
    
    products = [
         ["Puroduction","Items/Balles","Team" ,"Expense", "Production Date"],
    ]
    for purchase in purchase:
        products.append([
             
           purchase.Puroduction_Product_Name,purchase.Total_Production_Item,purchase.Production_Team_Name,  purchase.Total_Expense_Amount,purchase.date
        ])

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    paragraph_style = styles['Normal']

    # Define table style
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create invoice content
    content = []

    # Company details and logo
    company_logo = Image(company_logo_path, width=100, height=100)
    content.append(company_logo)
    content.append(Paragraph(company_name, title_style))
    content.append(Paragraph("Email: {}".format(company_email), paragraph_style))
    content.append(Paragraph("Head Office: {}".format(Head_Office), paragraph_style))
    content.append(Paragraph("Contact No.: {}".format(Phone), paragraph_style))
     

    # Client details
    content.append(Paragraph("____________________________________________", heading_style))
    content.append(Paragraph("Complete Purchase Report Of {}".format(request.user), heading_style))
    content.append(Paragraph("Created Date: {}".format(Date), paragraph_style))
    content.append(Paragraph("Total Expense:  {}".format(Total_Amount), paragraph_style)) 
    content.append(Paragraph("Total Vendor Production:  {}".format(vendor_total_Production), paragraph_style))
     
    content.append(Paragraph("", heading_style))

    # Invoice items table
    items_table = Table(products, colWidths=[200, 80, 80, 80])
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
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

def current_purchase_pdf(request):
    return render(request,'purchasepdf.html')
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
def Purchase_Filter(request):
    query = request.GET.get('query')
    results =  DailyProduction.objects.filter(Product_Name__icontains=query)
    return render(request,'PurchaseFilter.html',{'results':results,'query':query})
def VendorPurchaseSearch(request):
    query=request.GET.get("query")
    query2=request.GET.get("query2")
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    purchase=DailyProduction.objects.filter(user=request.user )
    if query:
        purchase =  purchase.filter(Puroduction_Product_Name__icontains=query)
    if query2:
        purchase = purchase.filter(Production_Place__icontains=query2)
    if fromdate and todate:
        purchase = purchase.filter(date__lte=todate, date__gte=fromdate) 
       
    compydetail=CompanyDetail.objects.all()
    
     
    Expense_Amount=Decimal(0.00)
    Grand_Total=Decimal(0.00)
    for purchases in purchase:
        Expense_Amount+=purchases.Total_Expense_Amount
    Grand_Total=Expense_Amount
    print(Grand_Total)

        
    comN=[]
    Email=[]
    address=[]
    phone=[]
    for com in compydetail:
        name=com.name
        comN.append(name)
        email=com.email
        Email.append(email)
        office=com.Head_Office
        address.append(office)
        Phone=com.phone
        phone.append(Phone)




    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="DailyProductionReport.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Define data for the invoice
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
     
    Head_Office = address[0]
    Phone = phone[0]
     
    Date= datetime.now().strftime("%d/%m/%Y")
    Total_Amount= Grand_Total
     
    
    
    products = [
         ["Puroduction","Items/Balles","Team" ,"Expense", "Date"],
    ]
    for purchase in purchase:
        products.append([
             
           purchase.Puroduction_Product_Name,purchase.Total_Production_Item,purchase.Production_Team_Name,  purchase.Total_Expense_Amount,purchase.date
        ])

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    paragraph_style = styles['Normal']

    # Define table style
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create invoice content
    content = []

    # Company details and logo
    company_logo = Image(company_logo_path, width=100, height=100)
    content.append(company_logo)
    content.append(Paragraph(company_name, title_style))
    content.append(Paragraph("{}".format(Head_Office), paragraph_style))
    content.append(Paragraph("{}".format(Phone), paragraph_style))
    content.append(Paragraph("{}".format(company_email), paragraph_style))
     

    # Client details
    content.append(Paragraph("____________________________________________", heading_style))
    content.append(Paragraph(" Daily Production Report Of {}".format(request.user), heading_style))
    content.append(Paragraph("Created Date: {}".format(Date), paragraph_style))
    content.append(Paragraph("Total Expense:  {}".format(Total_Amount), paragraph_style)) 
    
    
     
    content.append(Paragraph("", heading_style))

    # Invoice items table
    items_table = Table(products, colWidths=[200, 80, 80, 80])
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
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


def ManufacturePuchasePDF(request):
    query = request.GET.get("query")
    query2 = request.GET.get("query2")
    fromdate = request.GET.get("fromdate")
    todate = request.GET.get("todate")
    
    # Filter results based on queries
    results = Manufacturing.objects.filter(user=request.user)
    if query:
        results = results.filter(Manufacturing_Product_Name__icontains=query)
    if query2:
        results = results.filter(Place_Of_Supply__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)
    
    compydetail = CompanyDetail.objects.all()

    # Calculate totals
    Expense_Amount = Decimal(0.00)
    Total_Purchase = Decimal(0.00)
    Total_Sale = Decimal(0.00)

    for purchase in results:
        Expense_Amount += purchase.Manufacturing_Expense
        Total_Purchase += purchase.Total_Purchase_Price
        Total_Sale += purchase.Total_Sale_Amount

    Grand_Total_Expense = Expense_Amount
    Grand_Total_Purchase = Total_Purchase
    Grand_Total_Sale = Total_Sale
    Grand_Total_Profit_and_Lose = Grand_Total_Sale - Grand_Total_Purchase - Grand_Total_Expense

    # Get company details
    company_info = compydetail.first()
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual logo path
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ManufacturePurchaseReport.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    paragraph_style = styles['Normal']
    footer_style = ParagraphStyle('footer', fontSize=10, alignment=1, textColor=colors.black)

    # Data for the table
    products = [
        ["Bunkar",  "Balles", "Weight", "Total Weight", "Type", "Price", "Expenses", "Sale", "KG/Mund Rate"],
    ]
    for purchase in results:
        products.append([
            purchase.Manufacturing_Product_Name,
        
            purchase.Manufacture_Balles,
            purchase.Manufacture_Weight,
            purchase.Weight,
            purchase.Manufacturing_Purchase_Type,
            purchase.Total_Purchase_Price,
            purchase.Manufacturing_Expense,
            purchase.Total_Sale_Amount,

            purchase.Per_Kg_Or_Mund_Price,
        ])

    summary = [
        ["Total Purchase", "{:.2f}".format(Grand_Total_Purchase)],
        ["Total Expense", "{:.2f}".format(Grand_Total_Expense)],
        ["Total Sale", "{:.2f}".format(Grand_Total_Sale)],
        ["Profit/Loss", "{:.2f}".format(Grand_Total_Profit_and_Lose)]
    ]

    # Define table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Content for the PDF
    content = []

    # Company logo and details
    company_logo = Image(company_logo_path, width=100, height=100)
    content.append(company_logo)
    content.append(Paragraph(company_info.name, title_style))
    content.append(Paragraph(company_info.Head_Office, paragraph_style))
    content.append(Paragraph(company_info.phone, paragraph_style))
    content.append(Paragraph(company_info.email, paragraph_style))
    content.append(Spacer(1, 12))

    # Report title and date
    content.append(Paragraph(f"Report for {request.user}", heading_style))
    content.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y')}", paragraph_style))
    content.append(Spacer(1, 12))

    # Products table
    col_widths = [100, 60, 80, 80, 100, 60, 70, 60, 70]  # Adjust column widths for better responsiveness
    items_table = Table(products, colWidths=col_widths, hAlign='LEFT')
    items_table.setStyle(table_style)
    content.append(items_table)
    content.append(Spacer(1, 24))

    # Summary table
    summary_table = Table(summary, colWidths=[200, 100], hAlign='LEFT')
    summary_table.setStyle(table_style)
    content.append(summary_table)
    content.append(Spacer(1, 24))

    # Footer
    content.append(Paragraph("Powered by SoftApex Technologies", footer_style))

    # Build PDF
    pdf.build(content)

    return response
def ClientProfile(request,pk):
    clientdata=Client.objects.get(user=request.user,Whats_App_Number=pk)
    clientSale=Sale.objects.filter(user=request.user,Client_ID=pk)
    saleReturn=Sale_Return.objects.filter(user=request.user,Client_ID=pk)
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
      
def client_search(request):
    query = request.GET.get('query', '')
    if query:
        clients = Client.objects.filter(user=request.user,Full_Name__icontains=query)
    else:
        clients = Client.objects.all()
    
    client_data = [{'Whats_App_Number': client.Whats_App_Number, 'Full_Name': client.Full_Name} for client in clients]
    return JsonResponse({'clients': client_data})

def CurrentSale(request, pk):
    compydetail = CompanyDetail.objects.all()
    Invoice = Sale.objects.filter(user=request.user, Client_ID=pk).last()
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
    response['Content-Disposition'] = 'attachment; filename="SaleInvoice.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Define data for the invoice
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
    Head_Office = address[0]
    Phone = phone[0]
    Date = datetime.now().strftime("%d/%m/%Y")
    Client_Name = Invoice.Client_Name
    Client_ID=Invoice.Client_ID
    client_address = Invoice.Shiping_Address
    client_city = Invoice.Shipping_City
    client_mobile = Invoice.Client_Phone_Number
    client_state = Invoice.Shiping_State
    Driver_Name = Invoice.Driver_Name
    Driver_Contact = Invoice.Driver_Contact
    Vehicle_number = Invoice.Vehicle_Number
    Vehicle_Weight = Invoice.Vehicle_Weight
    Vehicle_Weight_Unit = Invoice.VECHCLE_WEIGHT_Unit
    Paid_Amount=Invoice.Paid_Amount
    Remaining=Invoice.Remaining
    Gst=Invoice.GST


    paymentstatus="Pending"
    if Invoice.Payment_Status==True:
        paymentstatus="Paid"

    sale = [
        ["Items/Balles", "Weight", "Unit", "Sale Price", "Total Amount", "Discount", "Final Amount"],
        [str(Invoice.Items_Or_Balles), str(Invoice.Weight), Invoice.Weight_Unit, str(Invoice.Sale_Price), str(Invoice.Total_Amount), str(Invoice.Discount), str(Invoice.Final_Amount)]
    ]

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
    company_logo = Image(company_logo_path, width=100, height=100)

    # Header and Company Details
    header_data = [
        [company_logo, Paragraph("<b>{}</b>".format(company_name), title_style)],
        ["", Paragraph("Email: {}".format(company_email), paragraph_style)],
        ["", Paragraph("Head Office: {}".format(Head_Office), paragraph_style)],
        ["", Paragraph("Contact No.: {}".format(Phone), paragraph_style)],
    ]

    header_table = Table(header_data, colWidths=[100, 400])
    content.append(header_table)
    content.append(Spacer(1, 12))
    invoice_number = random.randint(100000, 999999)
    # Client and Driver details in parallel
    client_driver_details = [
        ["Invoice Number",str(invoice_number), "Client ID", str(Client_ID)],
        ["Date", Date, "Driver Name", Driver_Name],
        ["Client Name", Client_Name, "Driver Contact", Driver_Contact],
        ["Paid Amount", str(Paid_Amount), "Pending Amount", str(Remaining)],
        ["Phone Number", client_mobile, "Vehicle Number", Vehicle_number],
        ["Shipping Address", client_address, "Vehicle Weight", str(Vehicle_Weight)],
        ["Shipping City", client_city, "Vehicle Weight Unit", Vehicle_Weight_Unit],
        ["Shipping State", client_state, "Payment Status", paymentstatus],
        ["GST", str(Gst), "Vendor ", request.user.username],
        
    ]

    details_data = [[Paragraph("<b>{}</b>".format(detail[0]), paragraph_style), Paragraph(detail[1], paragraph_style),
                     Paragraph("<b>{}</b>".format(detail[2]), paragraph_style), Paragraph(detail[3], paragraph_style)] for detail in client_driver_details]
    details_table = Table(details_data, colWidths=[150, 150, 150, 150])
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
    items_table = Table(sale, colWidths=[90, 90, 100, 50, 70, 100, 100, 60])
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
def currentInvoice(request,pk):
    customerid=pk
    compydetail = CompanyDetail.objects.first()
    Date = datetime.now().strftime("%d/%m/%Y")
    invoice_number = random.randint(100000, 999999)
    Invoice = Sale.objects.filter(user=request.user, Client_ID=pk).last()
    return render(request,'CurrentsalePDF.html',{'customerid':customerid,'invoice_number':invoice_number,'compydetail':compydetail,'invoice_number ':invoice_number,'Invoice':Invoice,'Date':Date })
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
 
def ClientReport(request, pk):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = Sale.objects.filter(user=request.user,Client_ID=pk)
    if query:
        results = results.filter(Sale_Production_Name__icontains=query)
    if query2:
        results = results.filter(Vehicle_Number__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)   
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
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
    Head_Office = address[0]
    Phone = phone[0]
    Date = datetime.now().strftime("%d/%m/%Y")
    client=Client.objects.get(user=request.user,Whats_App_Number=pk)
    Client_Name = client.Full_Name
    Client_ID=pk
    client_city = client.City
    client_mobile = client.Phone_Number
    client_state = client.State
    Total_Purchase_Amount=0
    Total_Pending_Amount=0
    Total_Paid_Amount=0
    
    for clientreport in results: 
        Total_Purchase_Amount+=clientreport.Total_Amount
        Total_Paid_Amount+=clientreport.Paid_Amount
        Total_Pending_Amount+=clientreport.Remaining



         
         
    
    sale = [
        ["Items/Balles", "Weight",  "Sale Price", "Total Amount", "Discount", "Final Amount","Pay Amount","Status"],]
    for report in results:
        paymentstatus="Pending"
      
        if report.Payment_Status==True:
           paymentstatus="Paid"
       
        sale.append([str(report.Items_Or_Balles), str(report.Weight),  str(report.Sale_Price), str(report.Total_Amount), str(report.Discount), str(report.Final_Amount),str(report.Paid_Amount),str(paymentstatus)]
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
        ["", Paragraph("Email: {}".format(company_email), paragraph_style)],
        ["", Paragraph("Head Office: {}".format(Head_Office), paragraph_style)],
        ["", Paragraph("Contact No.: {}".format(Phone), paragraph_style)],
    ]

    header_table = Table(header_data, colWidths=[100, 400])
    content.append(header_table)
    content.append(Spacer(1, 12))
    invoice_number = random.randint(100000, 999999)
    # Client and Driver details in parallel
    client_driver_details = [
        ["Report Number",str(invoice_number), "Client ID", str(Client_ID)],
        ["Date", Date, " Client Name ", Client_Name ],
        ["City", client_city, "State", client_state],
        ["Phone Number", client_mobile, "Total Purchase Amount", str(Total_Purchase_Amount)], 
        ["Total Paid Amount", str(Total_Paid_Amount), "Total Pending",  str(Total_Pending_Amount)],
        ["Seller Name", request.user.first_name, "Vendor ", request.user.username]
        
    ]

    details_data = [[Paragraph("<b>{}</b>".format(detail[0]), paragraph_style), Paragraph(detail[1], paragraph_style),
                     Paragraph("<b>{}</b>".format(detail[2]), paragraph_style), Paragraph(detail[3], paragraph_style)] for detail in client_driver_details]
    details_table = Table(details_data, colWidths=[150, 150, 150, 150])
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
def  SaleReport(request):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results = Sale.objects.filter(user=request.user)
    if query:
        results = results.filter(Client_Name__icontains=query)
    if query2:
        results = results.filter(Client_ID__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)   
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
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
    Head_Office = address[0]
    Phone = phone[0]
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
        ["Email", request.user.email, "Total Purchase Amount", str(Total_Purchase_Amount)], 
        ["Total Paid Amount", str(Total_Paid_Amount), "Total Pending",  str(Total_Pending_Amount)],
        ["Seller Name", request.user.first_name, "Vendor ", request.user.username]
        
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
 

def Itemchecking(request):
    items = request.POST.get('Sale_Production_Name')
    
    balles = int(request.POST.get('Items_Or_Balles'))  # Convert to integer
 
     
    item = Manufacturing.objects.get(Manufacturing_Product_Name=items)
    it = int(item.Total_Production_Items)
    
    if it < balles:
        print("working")
        return JsonResponse({'exists': True})
    
    return JsonResponse({'exists': False})
def currentPaymentInPdf(request,pk,id):
    customerid=pk
    return render(request,'PaymentInPDF.html',{'customerid':customerid,'id':id})
def paymentInSlip(request, pk,id):
    compydetail = CompanyDetail.objects.all()
    Invoice = Sale.objects.get(user=request.user, Client_ID=pk,id=id)
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
    response['Content-Disposition'] = 'attachment; filename="ClientPaidSlip.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Define data for the invoice
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
    Head_Office = address[0]
    Phone = phone[0]
    Date = datetime.now().strftime("%d/%m/%Y")
    Client_Name = Invoice.Client_Name
    Client_ID=Invoice.Client_ID
    client_address = Invoice.Shiping_Address
    client_city = Invoice.Shipping_City
    client_mobile = Invoice.Client_Phone_Number
    client_state = Invoice.Shiping_State
    Driver_Name = Invoice.Driver_Name
    Driver_Contact = Invoice.Driver_Contact
    Vehicle_number = Invoice.Vehicle_Number
    Vehicle_Weight = Invoice.Vehicle_Weight
    Vehicle_Weight_Unit = Invoice.VECHCLE_WEIGHT_Unit
    Paid_Amount=Invoice.Paid_Amount
    Remaining=Invoice.Remaining


    paymentstatus="Pending"
    if Invoice.Payment_Status==True:
        paymentstatus="Paid"

    sale = [
        ["Items/Balles", "Weight", "Unit", "Sale Price", "Total Amount", "Discount", "Final Amount"],
        [str(Invoice.Items_Or_Balles), str(Invoice.Weight), Invoice.Weight_Unit, str(Invoice.Sale_Price), str(Invoice.Total_Amount), str(Invoice.Discount), str(Invoice.Final_Amount)]
    ]

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
    company_logo = Image(company_logo_path, width=100, height=100)

    # Header and Company Details
    header_data = [
        [company_logo, Paragraph("<b>{}</b>".format(company_name), title_style)],
        ["", Paragraph("Email: {}".format(company_email), paragraph_style)],
        ["", Paragraph("Head Office: {}".format(Head_Office), paragraph_style)],
        ["", Paragraph("Contact No.: {}".format(Phone), paragraph_style)],
    ]

    header_table = Table(header_data, colWidths=[100, 400])
    content.append(header_table)
    content.append(Spacer(1, 12))
    invoice_number = random.randint(100000, 999999)
    # Client and Driver details in parallel
    client_driver_details = [
        ["Invoice Number",str(invoice_number), "Client ID", str(Client_ID)],
        ["Date", Date, "Driver Name", Driver_Name],
        ["Client Name", Client_Name, "Driver Contact", Driver_Contact],
        ["Paid Amount", str(Paid_Amount), "Pending Amount", str(Remaining)],
        ["Phone Number", client_mobile, "Vehicle Number", Vehicle_number],
        ["Shipping Address", client_address, "Vehicle Weight", str(Vehicle_Weight)],
        ["Shipping City", client_city, "Vehicle Weight Unit", Vehicle_Weight_Unit],
        ["Shipping State", client_state, "Payment Status", paymentstatus],
        ["Seller Name", request.user.first_name, "Vendor ", request.user.username],
        
    ]

    details_data = [[Paragraph("<b>{}</b>".format(detail[0]), paragraph_style), Paragraph(detail[1], paragraph_style),
                     Paragraph("<b>{}</b>".format(detail[2]), paragraph_style), Paragraph(detail[3], paragraph_style)] for detail in client_driver_details]
    details_table = Table(details_data, colWidths=[150, 150, 150, 150])
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
    items_table = Table(sale, colWidths=[90, 90, 100, 50, 70, 100, 100, 60])
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
def add_expense(request):
    compydetail = CompanyDetail.objects.first()
    balance = Profile.objects.get(user=request.user)
    productions = Manufacturing.objects.filter(user=request.user, Complete_Production=False)
    totalBalance = balance.Balance

    if request.method == 'POST':
        production_name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        harvesting_type = request.POST.get('harvesting-type')
        fuel_price = request.POST.get('fuel-price')
        total_Fuel = request.POST.get('total-fuel')
        Total_Acer = request.POST.get('total-acre')
        Price_Per_Acer = request.POST.get('harvest-price-per-acre')
        amount = Decimal(request.POST.get('amount'))
        payment_status = request.POST.get('payment_status')
        Paid_amount = request.POST.get('paid_amount')

        if not Paid_amount:  # Check if the value is empty or None
            Paid_amount = Decimal('0.0')
        else:
            Paid_amount = Decimal(Paid_amount)
        # Handling Remaining Amount
        print(Paid_amount)
        Remaining = request.POST.get('remaining_amount')
        if not Remaining:  # Check if the value is empty or None
            Remaining = Decimal('0.0')
        else:
            Remaining = Decimal(Remaining)
        bill = request.FILES['expensebill']
        notes = request.POST.get('notes')
        profile_instance= get_object_or_404(Profile, user=request.user)
        manufaccture_instance=Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=production_name)
 
        if category=="Harvesting":
            if harvesting_type=="Fuel":
                 manufaccture_instance.update(Harvesting_Cost=F("Harvesting_Cost")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount,Harvest_Type=harvesting_type,Total_Fuel=F("Total_Fuel")+total_Fuel,Fuel_Price=F("Fuel_Price")+fuel_price)
                 query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
                 query.save()
                 Profile.objects.filter(user=request.user).update(
                 Total_Expense=F("Total_Expense")+amount
        )
                 return redirect('expensebill')
            if harvesting_type=="Without Fuel":
                 manufaccture_instance.update(Harvesting_Cost=F("Harvesting_Cost")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount,Harvest_Type=harvesting_type,Total_Harvest_Acer=F("Total_Harvest_Acer")+Total_Acer,Harvest_Acer_Cost=F("Harvest_Acer_Cost")+Price_Per_Acer)
                 query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
                 query.save()
                 Profile.objects.filter(user=request.user).update(
                Total_Expense=F("Total_Expense")+amount
        )
                 return redirect('expensebill')
           
        elif  category=="Pressing":
            manufaccture_instance.update(Pressing_Cost=F("Pressing_Cost")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        elif  category=="Dumping":
            manufaccture_instance.update(Dumping_Cost=F("Dumping_Cost")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        elif  category=="Polythene":
            manufaccture_instance.update(Polythene_Cost=F("Polythene_Cost")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        elif  category=="Mud Cost":
            manufaccture_instance.update(Mud_Cost=F("Mud_Cost")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
    
                

        elif  category=="Balling Paper":
            manufaccture_instance.update(Packing_Material=F("Packing_Material")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        elif  category=="Stitch Paper":
            manufaccture_instance.update(Packing_Material=F("Packing_Material")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        elif  category=="Machine Depreciation":
            manufaccture_instance.update(Machine_Depreciation=F("Machine_Depreciation")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        elif  category=="Loading":
            manufaccture_instance.update(Loading_Cost=F("Loading_Cost")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        elif  category=="Labour":
            manufaccture_instance.update(Labour_Expense=F("Labour_Expense")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes)
            query.save()
            Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        else:
            manufaccture_instance.update(Other_Expense=F("Other_Expense")+amount,Manufacturing_Expense=F("Manufacturing_Expense")+amount)
            query=Expense.objects.create(user=request.user,userprofile=profile_instance,Production_Name=production_name,description=description,category=category,amount=amount,Bill_Proof=bill,notes=notes,Payment_Status=payment_status,Paid_Amount=Paid_amount,Remaining_Amount=Remaining)
            query.save()
        Profile.objects.filter(user=request.user).update(
            Total_Expense=F("Total_Expense")+amount
        )
        # Redirect to a success page or do further processing
        return redirect('expensebill')  # Replace with your success URL or view name
    if request.htmx:
        return render(request,'components/expense_form.html',{'totalBalance':totalBalance,'productions':productions,'compydetail':compydetail})
    else:
        return render(request, 'expense_form.html',{'totalBalance':totalBalance,'productions':productions,'compydetail':compydetail})
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
def expensebill(request):
    return render(request,"expensebill.html") 
 
def generate_expense_report(request):
    # Fetch data from the database
    results  = Expense.objects.filter(user=request.user)
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)   
    # Calculate totals
    total_amount = Decimal(0.00)
    for expense in results:
        total_amount += expense.amount

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="ExpenseReport.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    
    # Fetch company details (assuming there's only one company)
    try:
        company_detail = CompanyDetail.objects.get()
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
    content.append(Paragraph("Expense Report", heading_style))
    content.append(Paragraph("Report Date: {}".format(date), paragraph_style))
    content.append(Spacer(1, 20))

    # Expenses table
    data = [
        ["Description","Category", "Amount", "Date"]
    ]
    for expns in results:
        data.append([expns.description,expns.category, "{:.2f}".format(expns.amount), expns.date.strftime("%d/%m/%Y")])

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

def ExpenseSlip(request):
    # Fetch data from the database
    expenses = Expense.objects.filter(user=request.user).last()
    


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="ExpenseReport.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    
    # Fetch company details (assuming there's only one company)
    try:
        company_detail = CompanyDetail.objects.get()
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
    content.append(Paragraph("Expense Report", heading_style))
    content.append(Paragraph("Report Date: {}".format(date), paragraph_style))
    content.append(Spacer(1, 20))

    # Expenses table
    data = [
        ["Description","Category", "Amount", "Date"]
    ]
     
    data.append([expenses.description,expenses.category, "{:.2f}".format(expenses.amount), expenses.date.strftime("%d/%m/%Y")])

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

    
    # Footer
    content.append(Paragraph("", footer_style))

    # Build the PDF document
    pdf.build(content)
    return response
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
def PaymentOutSlip(request):
    # Fetch the last expense record for the user
    expenses = PaymentOut.objects.filter(user=request.user).last()

    # Set up the response and PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PaymentOutSlip.pdf"'
    pdf = SimpleDocTemplate(response, pagesize=letter)
    
    # Fetch company details (assuming there's only one company)
    try:
        company_detail = CompanyDetail.objects.get()
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
def withdrwalSlip(request):
    return render(request,"WithdrwalSlip.html")
 
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
        company_detail = CompanyDetail.objects.get()
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
def  SaleReturnReport(request):
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
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
    Head_Office = address[0]
    Phone = phone[0]
    Date = datetime.now().strftime("%d/%m/%Y")
    Total_Return_Amount=0
    
    for salereport in results: 
        Total_Return_Amount+=salereport.Return_To_Customer_Amount
         


         
         
    
    sale = [
        ["Client","Production","Items/Balles", "Weight",  "Return Amount"],]
    for report in results:
        
       
          
           
        sale.append([str(report.Client_Name),str(report.Sale_Production_Name),str(report.Items_Or_Balles), str(report.Weight),  str(report.Return_To_Customer_Amount),]
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
        ["Email", request.user.email, "Total Return", str(Total_Return_Amount)], 
        ["Seller Name",request.user.first_name, "Vendor ", request.user.username]
        
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
    items_table = Table(sale, colWidths=[120, 60, 90, 80, 80, 70, 80, 70])
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
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
 
def generate_daily_report():
    today = date.today()
    
    # Fetch company details
    try:
        company_detail = CompanyDetail.objects.get()
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

       
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_daily_report, 'interval', hour=0,minute=0,second=0)  # Adjust time as needed
    scheduler.start()

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
def FraudDector(request):
    mail=Profile.objects.get(user=request.user)
    alert=mail.email

    subject = f'Fraud Have Been Detected From Admin'
    message = (
        f'Dear {request.user}. The Record Of Your Sales Have Been Change By The Admin Please Take Action To Resolve the Issues\n\n'
         
    )
    send_mail(subject, message,  settings.EMAIL_HOST_USER, [alert])
     
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal, InvalidOperation

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
        Total_Amount_Weight = request.POST.get("Wtotal")
        profile_instance = get_object_or_404(Profile, user=request.user)
        
        check = Manufacturing.objects.filter(Manufacturing_Product_Name=BunkarName).exists()
        if check:
            messages.warning(request, 'Bankar Name Already Exist, Please Enter Unique Bunkar Name')
            return redirect('AddManufecturePurchase')
        
        try:
            total_amount_acers = Decimal(total_amount_acers_str) if total_amount_acers_str else Decimal(0)
        except InvalidOperation:
            messages.error(request, "Invalid amount format for total_amount_acers.")
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
                Total_Purchase_Price=total_amount_acers
            )
            messages.info(request, "Bunkar Record Added! Please Add Expense Of Your New Bunkar")
            return redirect("add_expense")
        
        if Purchase_Type == "PURCHASE_WEIGHT":
            if total_amount_acers <= 0:
                messages.info(request, "Please Fill All Calculation Fields")
                return redirect("add_expense")

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
                Total_Purchase_Price=Total_Amount_Weight
            )
            messages.info(request, "Bunkar Record Added! Please Add Expense Of Your New Bunkar")
            return redirect("add_expense")

    if request.htmx:
        return render(request, "components/Purchaseform.html")
    else:
        return render(request, 'ManufacturePurchaseForm.html')

def HarvestingExpense(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Harvesting.html",{'productions':productions})
    else:
        return render(request,'Harvesting.html',{'productions':productions})
def Dumping(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Dumping.html",{'productions':productions})
    else:
        return render(request,'Dumping.html',{'productions':productions})
def Polythene(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Polythene.html",{'productions':productions})
    else:
        return render(request,'Polythene.html',{'productions':productions})
def PackingMaterial(request):
    productions=Manufacturing.objects.filter(user=request.user,Complete_Production=False)
    if request.htmx:
        return render(request,"components/Packing.html",{'productions':productions})
    else:
        return render(request,'Packing.html',{'productions':productions})
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
        return redirect('AddDailyProduction')  # Redirect to a list view or another view
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
            Payment_Status=payment_status
        )
        
        messages.success(request, "Loading Labour Record data added successfully!")
        return redirect('Vendor')  # Redirect to a list view or another view

    return render(request, 'add_loading_labour_record.html',{'productions':productions,'labour':labour})
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

def generate_Production_Labour_report(request):
    # Fetch data from the database
    results  = LoadingLabourRecord.objects.filter(user=request.user)
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)   
    # Calculate totals
    total_amount = Decimal(0.00)
    for expense in results:
        total_amount += expense.Total_Amount

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="Production_Labour_Expense_Report.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))
    
    # Fetch company details (assuming there's only one company)
    try:
        company_detail = CompanyDetail.objects.get()
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
    content.append(Paragraph("Production Labour Record", heading_style))
    content.append(Paragraph("Report Date: {}".format(date), paragraph_style))
    content.append(Spacer(1, 20))

    # Expenses table
    data = [
        ["Leader","Bunkar","Bales", "Bale Price", "Total","Status","Date"]
    ]
    for expns in results:
        data.append([expns.Team_Leader,expns.Bankar,"{:.2f}".format(expns.Bales), "{:.2f}".format(expns.Per_Bale_Price), "{:.2f}".format(expns.Total_Amount), expns.Payment_Status ,expns.date.strftime("%d/%m/%Y")])

    col_widths = [100,130, 100, 90,90,90,100]  # Adjust column widths
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

def generate_Loading_Labour_report(request):
    # Fetch data from the database
    results  = LoadingLabourRecord.objects.filter(user=request.user)
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)   
    # Calculate totals
    total_amount = Decimal(0.00)
    for expense in results:
        total_amount += expense.Total_Amount

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="Loading_Labour_Expense_Report.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))
    
    # Fetch company details (assuming there's only one company)
    try:
        company_detail = CompanyDetail.objects.get()
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
    content.append(Paragraph("Loading Labour Record", heading_style))
    content.append(Paragraph("Report Date: {}".format(date), paragraph_style))
    content.append(Spacer(1, 20))

    # Expenses table
    data = [
        ["Leader","Bunkar","Bales", "Bale Price", "Total","Status","Date"]
    ]
    for expns in results:
        data.append([expns.Team_Leader,expns.Bankar,"{:.2f}".format(expns.Bales), "{:.2f}".format(expns.Per_Bale_Price), "{:.2f}".format(expns.Total_Amount), expns.Payment_Status ,expns.date.strftime("%d/%m/%Y")])

    col_widths = [100,130, 100, 90,90,90,100]  # Adjust column widths
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
def CreditToPaid(request, id):
    if request.method == "POST":
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
 
def CreditToPaidLoading(request, id):
    if request.method == "POST":
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


 
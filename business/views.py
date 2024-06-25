from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
from datetime import datetime,timedelta
from django.db.models import F
from django.db.models import Sum
from django.template.loader import render_to_string,get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
import pandas as pd
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.db.models.functions import ExtractYear, ExtractMonth
from django.conf import settings
from django.core.mail import EmailMessage
from .models import *
def index(request):
    compydetail=CompanyDetail.objects.all()
    return render(request,"index.html", {'compydetail':compydetail})
def Vendor(request):
    query = request.GET.get('query')
    query2=request.GET.get('query2')
    fromdate=request.GET.get("fromdate")
    todate=request.GET.get('todate')
    results =  Manufacturing.objects.filter(user=request.user)
    # Apply additional filters if they are provided
    if query:
        results = results.filter(Puroduction_Product_Name__icontains=query)
    if query2:
        results = results.filter(Production_Place__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)    
    
    manufacture=Manufacturing.objects.filter(user=request.user)

    print(manufacture)

    if request.htmx:
        return render(request, 'components/Vendor.html',{'manufacture':manufacture})
    else:

      return render(request,"Vendor.html",{'manufacture':manufacture})
    
def Addclient(request):
    compydetail=CompanyDetail.objects.all()
    if request.method=="POST":
        name=request.POST.get("fullname")
        email=request.POST.get("email")
        whatsappno=request.POST.get("WhatsAppNo")
        phoneno=request.POST.get("mnumber")
        address=request.POST.get("address")
        city=request.POST.get("city")
        state=request.POST.get("state")
        bname=request.POST.get("bname")
        accountType=request.POST.get("accountType")
        openingBalance=request.POST.get("openbalance",'')
        creditlimit=request.POST.get("creditLimit",'')
        query=Client.objects.create(user=request.user,Full_Name=name,Email=email,Whats_App_Number=whatsappno,Phone_Number=phoneno,Billing_Address=address,City=city,State=state,Business_Name=bname,Acccount_Type=accountType,Opening_Balance=openingBalance,Credit_Limit=creditlimit)
        query.save()
        return redirect("Vendor")
    if request.htmx:
        return render(request, 'components/AddClient.html',{'compydetail': compydetail})
    else:
        return render(request,"client.html",{'compydetail': compydetail})
     

   
     
def AddDailyProduction(request):
    compydetail=CompanyDetail.objects.all()
    Email=[]
    for com in compydetail:
        email=com.email
        Email.append(email)
    Products=Manufacturing.objects.filter(user=request.user,Complete_Production=False).all()
    if request.method=="POST":
        Puroduction_Product_Name=request.POST.get("Production_Product_Name")
        print(Puroduction_Product_Name)
        Production_Place=request.POST.get("Production_Place")
        city=request.POST.get("city")
        Total_Production_Item=request.POST.get("Total_Production_Item")
        Production_and_Expense_Proof_Screenshot=request.FILES["Production_and_Expense_Proof_Screenshot"]
        Production_Team_Name=request.POST.get("Production_Team_Name")
        Total_Expense_Amount=request.POST.get("Total_Expense_Amount")
        Expense_Remarks=request.POST.get("Remarks_of_Expense")
        Production_completed=request.POST.get("Settlement")
        query=DailyProduction.objects.create(user=request.user, Puroduction_Product_Name=Puroduction_Product_Name,Production_Place=Production_Place, City=city,Total_Production_Item=Total_Production_Item,Production_and_Expense_Proof_Screenshot=Production_and_Expense_Proof_Screenshot, Production_Team_Name= Production_Team_Name,Total_Expense_Amount=Total_Expense_Amount,Remarks_of_Expense=Expense_Remarks )
        query.save()
        items=int(Total_Production_Item)
        expense=int(Total_Expense_Amount)
        if  Production_completed=="complete":
            print("good")
            Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=Puroduction_Product_Name).update(
            Complete_Production=True

    )
        Manufacturing.objects.filter(user=request.user,Manufacturing_Product_Name=Puroduction_Product_Name).update(
        Total_Production_Items=F('Total_Production_Items') + items,Manufacturing_Expense=F('Manufacturing_Expense')+expense

    )
        
         
        email_subject = "Daily Production Detail"
        message = render_to_string('DailyproductionEmail.html', {
                    'SiteName':request.user,
                    'Production_Name':Puroduction_Product_Name,
                    'item_or_Balles':items,
                    'Production_Team':Production_Team_Name,
                    'Production_Place':Production_Place,
                    'Production_Status':Production_completed,
                    'Expense':Total_Expense_Amount,
                    'Expense_Remark':Expense_Remarks,
              
        })
        email_message2 = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, Email,)
        email_message2.send()

    
         
    
        
            

       

        return redirect("current_purchase_pdf")
    if request.htmx:
        return render(request, 'components/AddPurchase.html',{'compydetail': compydetail,'Products': Products})
    else:
        return render(request,"Addpurchase.html",{'compydetail': compydetail,'Products': Products})
 
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
        exists = DailyProduction.objects.filter(Product_Name=product_name).exists()
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
    response['Content-Disposition'] = 'attachment; filename="NewPurchase.pdf"'

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
        ["Puroduction","Items/Balles","Production Team" ,"Expense", "Production Date"],
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
    content.append(Paragraph("Purchase Invoice", heading_style))
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
    response['Content-Disposition'] = 'attachment; filename="TotalPurchase.pdf"'

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
         ["Puroduction","Items/Balles","Production Team" ,"Expense", "Production Date"],
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
    response['Content-Disposition'] = 'attachment;filename="TotalPurchase.pdf"'

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
         ["Puroduction","Items/Balles","Production Team" ,"Expense", "Production Date"],
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
    content.append(Paragraph("Purchase Report Of {}".format(request.user), heading_style))
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
    todate = request.GET.get('todate')
    results = Manufacturing.objects.filter(user=request.user)
    if query:
        results = results.filter(Manufacturing_Product_Name__icontains=query)
    if query2:
        results = results.filter(Place_Of_Supply__icontains=query2)
    if fromdate and todate:
        results = results.filter(date__lte=todate, date__gte=fromdate)
    compydetail = CompanyDetail.objects.all()
    Expense_Amount=Decimal(0.00)
    Grand_Total_Expense=Decimal(0.00)
    Total_Purchase=Decimal(0.00)
    Grand_Total_Purchase=Decimal(0.00)
    Total_Sale=Decimal(0.00)
    Grand_Total_Sale=Decimal(0.00)

    for purchases in results:
        Expense_Amount+=purchases.Manufacturing_Expense
        Total_Purchase+=purchases.Total_Purchase_Price
        Total_Sale+=purchases.Total_Sale_Amount

    Grand_Total_Expense=Expense_Amount
    Grand_Total_Purchase=Total_Purchase
    Grand_Total_Sale=Total_Sale
    Grand_Total_Profit_and_Lose= Grand_Total_Sale-Grand_Total_Purchase-Grand_Total_Expense

     
    
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
    response['Content-Disposition'] = 'attachment;filename="TotalPurchase.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=landscape(letter))  # Change to landscape mode

    # Define data for the invoice
    company_logo_path = "media/Company Logo/logo1.png"  # Replace with actual path
    company_name = comN[0]
    company_email = Email[0]
    Head_Office = address[0]
    Phone = phone[0]
    Date = datetime.now().strftime("%d/%m/%Y")
    
    products = [
        ["Production", "Items/Balles" , "Weight ","Unit" ,"Purchase Price", "Manufacturing Expense", "Total Sale", "Profit/Lose"],
    ]
    for purchase in results:
        products.append([
            purchase.Manufacturing_Product_Name, purchase.Total_Production_Items,  purchase.Weight, purchase.Unit, purchase.Total_Purchase_Price, purchase.Manufacturing_Expense, purchase.Total_Sale_Amount, purchase.Profit_OR_Lose,
        ])

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    paragraph_style = styles['Normal']

    # Define table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

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
    content.append(Paragraph("___________________________________________________________", heading_style))
    content.append(Paragraph("Purchase Report Of {}".format(request.user), heading_style))
    content.append(Paragraph("Report Date: {}".format(Date), paragraph_style))
    content.append(Paragraph("Total Purchase: {}".format(Grand_Total_Purchase), paragraph_style))
    content.append(Paragraph("Total Expense: {}".format(Grand_Total_Expense), paragraph_style))
    content.append(Paragraph("Total Sale: {}".format(Grand_Total_Sale), paragraph_style))
    content.append(Paragraph("Profit/Lose: {}".format(Grand_Total_Profit_and_Lose), paragraph_style))
    content.append(Paragraph("", heading_style))

    # Invoice items table
    col_widths = [100, 80, 100, 80, 120, 120, 120, 60, 60]  # Adjust column widths
    items_table = Table(products, colWidths=col_widths)
    items_table.setStyle(table_style)
    content.append(items_table)

    # Build the PDF document
    pdf.build(content)
    return response
def ClientProfile(request,pk):
    clientdata=Client.objects.filter(user=request.user,Whats_App_Number=pk)
    print(clientdata)
    if request.htmx:
        return render(request, 'components/Clientprofile.html')
    else:
      return render(request,"Clientprofile.html")
    
   
       


   
    

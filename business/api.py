from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime
from .models import *
from .views import calculate_monthly_total, calculate_monthly_Sale, calculate_monthly_Pending, calculate_monthly_received


class DashboardAPIView(APIView):
    """
    API endpoint for dashboard data including vendor analytics
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            current_year = datetime.now().year
            
            # Monthly totals for the current year
            monthly_purchase_data = {}
            monthly_sales_data = {}
            monthly_received_data = {}
            monthly_pending_data = {}
            
            months = [
                'january', 'february', 'march', 'april', 'may', 'june',
                'july', 'august', 'september', 'october', 'november', 'december'
            ]
            
            # Calculate monthly data
            for i, month in enumerate(months, 1):
                monthly_purchase_data[month] = float(calculate_monthly_total(request, current_year, i))
                monthly_sales_data[month] = float(calculate_monthly_Sale(request, current_year, i))
                monthly_received_data[month] = float(calculate_monthly_received(request, current_year, i))
                monthly_pending_data[month] = float(calculate_monthly_Pending(request, current_year, i))
            
            # Get recent sales
            recent_sales = Sale.objects.filter(user=user).order_by('-date')[:10]
            recent_sales_data = []
            for sale in recent_sales:
                recent_sales_data.append({
                    'id': sale.id,
                    'client_name': sale.Client_Name,
                    'production_name': sale.Sale_Production_Name,
                    'total_amount': float(sale.Total_Amount),
                    'paid_amount': float(sale.Paid_Amount),
                    'remaining': float(sale.Remaining),
                    'payment_status': sale.Payment_Status,
                    'date': sale.date.strftime('%Y-%m-%d')
                })
            
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
            total_received_payment = sales.aggregate(total=Sum('Paid_Amount'))['total'] or Decimal(0.00)
            
            siteexp = withdrawals.aggregate(total=Sum('amount'))['total'] or Decimal(0.00)
            
            # Profit calculation
            profit = total_sale - total_purchase - manufacture_expense
            site_profit = profit - siteexp
            
            # Credit calculations
            credit_amount = loading_labour_credit.aggregate(total=Sum('Remaining'))['total'] or Decimal(0.00)
            credit_amount_pro = production_labour_credit.aggregate(total=Sum('Remaining'))['total'] or Decimal(0.00)
            expense_credit = expenses_credit.aggregate(total=Sum('Remaining_Amount'))['total'] or Decimal(0.00)
            manufacturing_credit_amount = manufacturing_credit.aggregate(total=Sum('Remaining_Amount'))['total'] or Decimal(0.00)
            
            # Dashboard data
            dashboard_data = {
                'financial_summary': {
                    'total_purchase': float(total_purchase),
                    'total_sales': float(total_sales),
                    'total_pending': float(total_pending),
                    'total_received_payment': float(total_received_payment),
                    'site_expenses': float(siteexp),
                    'manufacture_expense': float(manufacture_expense),
                    'profit': float(profit),
                    'site_profit': float(site_profit)
                },
                'monthly_data': {
                    'purchase': monthly_purchase_data,
                    'sales': monthly_sales_data,
                    'received': monthly_received_data,
                    'pending': monthly_pending_data
                },
                'credit_summary': {
                    'loading_labour_credit': float(credit_amount),
                    'production_labour_credit': float(credit_amount_pro),
                    'expense_credit': float(expense_credit),
                    'manufacturing_credit': float(manufacturing_credit_amount)
                },
                'recent_sales': recent_sales_data,
                'user_info': {
                    'username': user.username,
                    'email': user.email,
                    'company_name': user.company_name or '',
                    'phone_number': user.phone_number or ''
                }
            }
            
            return Response(dashboard_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching dashboard data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SalesAPIView(APIView):
    """
    API endpoint for sales data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # Get query parameters for filtering
            client_name = request.query_params.get('client_name', None)
            from_date = request.query_params.get('from_date', None)
            to_date = request.query_params.get('to_date', None)
            payment_status = request.query_params.get('payment_status', None)
            
            # Base queryset
            sales = Sale.objects.filter(user=user)
            
            # Apply filters
            if client_name:
                sales = sales.filter(Client_Name__icontains=client_name)
            
            if from_date:
                sales = sales.filter(date__gte=from_date)
            
            if to_date:
                sales = sales.filter(date__lte=to_date)
            
            if payment_status is not None:
                sales = sales.filter(Payment_Status=payment_status.lower() == 'true')
            
            # Order by date (newest first)
            sales = sales.order_by('-date')
            
            # Prepare sales data
            sales_data = []
            for sale in sales:
                sales_data.append({
                    'id': sale.id,
                    'client_name': sale.Client_Name,
                    'client_phone': sale.Client_Phone_Number,
                    'production_name': sale.Sale_Production_Name,
                    'items_or_balles': sale.Items_Or_Balles,
                    'weight': float(sale.Weight),
                    'weight_unit': sale.Weight_Unit,
                    'sale_price': float(sale.Sale_Price),
                    'total_amount': float(sale.Total_Amount),
                    'discount': float(sale.Discount) if sale.Discount else 0,
                    'final_amount': float(sale.Final_Amount) if sale.Final_Amount else 0,
                    'paid_amount': float(sale.Paid_Amount),
                    'remaining': float(sale.Remaining) if sale.Remaining else 0,
                    'payment_status': sale.Payment_Status,
                    'shipping_address': sale.Shiping_Address,
                    'shipping_city': sale.Shipping_City,
                    'shipping_state': sale.Shiping_State,
                    'driver_name': sale.Driver_Name,
                    'vehicle_number': sale.Vehicle_Number,
                    'driver_contact': sale.Driver_Contact,
                    'gst': float(sale.GST) if sale.GST else 0,
                    'date': sale.date.strftime('%Y-%m-%d')
                })
            
            # Calculate totals
            total_amount = sum(float(sale.Total_Amount) for sale in sales)
            total_paid = sum(float(sale.Paid_Amount) for sale in sales)
            total_remaining = sum(float(sale.Remaining) if sale.Remaining else 0 for sale in sales)
            
            return Response({
                'sales': sales_data,
                'summary': {
                    'total_sales': len(sales_data),
                    'total_amount': total_amount,
                    'total_paid': total_paid,
                    'total_remaining': total_remaining
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching sales data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ManufacturingAPIView(APIView):
    """
    API endpoint for manufacturing data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # Get query parameters for filtering
            product_name = request.query_params.get('product_name', None)
            supplier_name = request.query_params.get('supplier_name', None)
            from_date = request.query_params.get('from_date', None)
            to_date = request.query_params.get('to_date', None)
            
            # Base queryset
            manufacturing = Manufacturing.objects.filter(user=user)
            
            # Apply filters
            if product_name:
                manufacturing = manufacturing.filter(Manufacturing_Product_Name__icontains=product_name)
            
            if supplier_name:
                manufacturing = manufacturing.filter(Supplier_Name__icontains=supplier_name)
            
            if from_date:
                manufacturing = manufacturing.filter(date__gte=from_date)
            
            if to_date:
                manufacturing = manufacturing.filter(date__lte=to_date)
            
            # Order by date (newest first)
            manufacturing = manufacturing.order_by('-date')
            
            # Prepare manufacturing data
            manufacturing_data = []
            for item in manufacturing:
                manufacturing_data.append({
                    'product_name': item.Manufacturing_Product_Name,
                    'supplier_name': item.Supplier_Name,
                    'place_of_supply': item.Place_Of_Supply,
                    'purchase_type': item.Manufacturing_Purchase_Type,
                    'total_acers': float(item.Total_Acers),
                    'per_acer_price': float(item.Per_Acer_Purchase_Price),
                    'weight': float(item.Weight),
                    'manufacture_weight': float(item.Manufacture_Weight),
                    'total_production_items': item.Total_Production_Items,
                    'manufacture_balles': item.Manufacture_Balles,
                    'total_purchase_price': float(item.Total_Purchase_Price),
                    'manufacturing_expense': float(item.Manufacturing_Expense),
                    'total_sale_amount': float(item.Total_Sale_Amount) if item.Total_Sale_Amount else 0,
                    'profit_or_loss': float(item.Profit_OR_Lose) if item.Profit_OR_Lose else 0,
                    'complete_production': item.Complete_Production,
                    'out_of_stock': item.Out_Of_Stock,
                    'payment_status': item.Payment_Status,
                    'date': item.date.strftime('%Y-%m-%d')
                })
            
            # Calculate totals
            total_purchase = sum(float(item.Total_Purchase_Price) for item in manufacturing)
            total_expense = sum(float(item.Manufacturing_Expense) for item in manufacturing)
            total_sale = sum(float(item.Total_Sale_Amount) if item.Total_Sale_Amount else 0 for item in manufacturing)
            total_profit = total_sale - total_purchase - total_expense
            
            return Response({
                'manufacturing': manufacturing_data,
                'summary': {
                    'total_items': len(manufacturing_data),
                    'total_purchase': total_purchase,
                    'total_expense': total_expense,
                    'total_sale': total_sale,
                    'total_profit': total_profit
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching manufacturing data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpensesAPIView(APIView):
    """
    API endpoint for expenses data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # Get query parameters for filtering
            category = request.query_params.get('category', None)
            from_date = request.query_params.get('from_date', None)
            to_date = request.query_params.get('to_date', None)
            payment_status = request.query_params.get('payment_status', None)
            
            # Base queryset
            expenses = Expense.objects.filter(user=user)
            
            # Apply filters
            if category:
                expenses = expenses.filter(category=category)
            
            if from_date:
                expenses = expenses.filter(date__gte=from_date)
            
            if to_date:
                expenses = expenses.filter(date__lte=to_date)
            
            if payment_status:
                expenses = expenses.filter(Payment_Status=payment_status)
            
            # Order by date (newest first)
            expenses = expenses.order_by('-date')
            
            # Prepare expenses data
            expenses_data = []
            for expense in expenses:
                expenses_data.append({
                    'id': expense.id,
                    'production_name': expense.Production_Name,
                    'description': expense.description,
                    'category': expense.category,
                    'amount': float(expense.amount),
                    'paid_amount': float(expense.Paid_Amount) if expense.Paid_Amount else 0,
                    'remaining_amount': float(expense.Remaining_Amount) if expense.Remaining_Amount else 0,
                    'payment_status': expense.Payment_Status,
                    'notes': expense.notes,
                    'date': expense.date.strftime('%Y-%m-%d')
                })
            
            # Calculate totals
            total_amount = sum(float(expense.amount) for expense in expenses)
            total_paid = sum(float(expense.Paid_Amount) if expense.Paid_Amount else 0 for expense in expenses)
            total_remaining = sum(float(expense.Remaining_Amount) if expense.Remaining_Amount else 0 for expense in expenses)
            
            return Response({
                'expenses': expenses_data,
                'summary': {
                    'total_expenses': len(expenses_data),
                    'total_amount': total_amount,
                    'total_paid': total_paid,
                    'total_remaining': total_remaining
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching expenses data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientsAPIView(APIView):
    """
    API endpoint for clients data
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            
            # Get query parameters for filtering
            name = request.query_params.get('name', None)
            city = request.query_params.get('city', None)
            
            # Base queryset
            clients = Client.objects.filter(user=user)
            
            # Apply filters
            if name:
                clients = clients.filter(Full_Name__icontains=name)
            
            if city:
                clients = clients.filter(City__icontains=city)
            
            # Prepare clients data
            clients_data = []
            for client in clients:
                # Calculate client's purchase history
                client_sales = Sale.objects.filter(user=user, Client_ID=client)
                total_purchases = client_sales.aggregate(total=Sum('Total_Amount'))['total'] or 0
                total_paid = client_sales.aggregate(total=Sum('Paid_Amount'))['total'] or 0
                total_pending = client_sales.aggregate(total=Sum('Remaining'))['total'] or 0
                
                clients_data.append({
                    'id': client.Whats_App_Numbe,
                    'full_name': client.Full_Name,
                    'email': client.Email,
                    'whatsapp_number': client.Whats_App_Number,
                    'phone_number': client.Phone_Number,
                    'billing_address': client.Billing_Address,
                    'city': client.City,
                    'state': client.State,
                    'business_name': client.Business_Name,
                    'account_type': client.Acccount_Type,
                    'opening_balance': float(client.Opening_Balance) if client.Opening_Balance else 0,
                    'credit_limit': float(client.Credit_Limit) if client.Credit_Limit else 0,
                    'total_purchases': float(total_purchases),
                    'total_paid': float(total_paid),
                    'total_pending': float(total_pending)
                })
            
            return Response({
                'clients': clients_data,
                'summary': {
                    'total_clients': len(clients_data)
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching clients data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

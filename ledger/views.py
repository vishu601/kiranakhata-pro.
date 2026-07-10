from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import ShopkeeperSignUpForm
from .models import Customer, Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.contrib import messages
from decimal import Decimal

def signup_view(request):
    if request.method == 'POST':
        form = ShopkeeperSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ShopkeeperSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard_view(request):
    shopkeeper = request.user
    
    # --- HANDLE POST REQUESTS (Quick Actions) ---
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Add New Customer
        if action == 'add_customer':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            limit = request.POST.get('credit_limit', 5000)
            if name:
                Customer.objects.create(shopkeeper=shopkeeper, name=name, phone=phone, credit_limit=limit)
                messages.success(request, f"Grahak '{name}' ko register kar diya gaya hai!")
            return redirect('dashboard')
            
        # Add Transaction (Udhaar / Jama)
        elif action == 'add_transaction':
            customer_id = request.POST.get('customer_id')
            amount = request.POST.get('amount')
            t_type = request.POST.get('transaction_type')
            desc = request.POST.get('description', '')
            
            if customer_id and amount:
                customer = get_object_or_404(Customer, id=customer_id, shopkeeper=shopkeeper)
                Transaction.objects.create(
                    customer=customer,
                    amount=Decimal(amount),
                    transaction_type=t_type,
                    description=desc
                )
                messages.success(request, f"₹{amount} ka transaction successful!")
            return redirect('dashboard')

    # --- SEARCH & FILTERING ---
    search_query = request.GET.get('search', '')
    customers_queryset = Customer.objects.filter(shopkeeper=shopkeeper)
    if search_query:
        customers_queryset = customers_queryset.filter(
            Q(name__icontains=search_query) | Q(phone__icontains=search_query)
        )

    # --- DATA CALCULATION FOR TEMPLATE ---
    customers_data = []
    total_market_udhaar = Decimal('0.00')
    total_customers_count = customers_queryset.count()
    
    for cust in customers_queryset:
        udhaar = cust.transactions.filter(transaction_type='UDHAAR').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        jama = cust.transactions.filter(transaction_type='JAMA').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        net_balance = udhaar - jama
        
        is_alert = net_balance >= (cust.credit_limit * Decimal('0.8'))
        
        customers_data.append({
            'obj': cust,
            'net_balance': net_balance,
            'abs_balance': abs(net_balance),  # Backend par hi minus sign saaf kar diya
            'is_alert': is_alert,
            'transactions': cust.transactions.all().order_by('-date')[:5]
        })
        
        if net_balance > 0:
            total_market_udhaar += net_balance

    # Today's Recovery
    from django.utils import timezone
    today = timezone.now().date()
    todays_recovery = Transaction.objects.filter(
        customer__shopkeeper=shopkeeper, 
        transaction_type='JAMA',
        date__date=today
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    context = {
        'username': shopkeeper.username,
        'customers_data': customers_data,
        'total_customers': total_customers_count,
        'total_market_udhaar': total_market_udhaar,
        'todays_recovery': todays_recovery,
        'search_query': search_query,
    }
    return render(request, 'ledger/dashboard.html', context)
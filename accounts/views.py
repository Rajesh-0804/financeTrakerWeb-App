# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from django.db.models import Sum
import json

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user)

    # ✅ Step 1: Totals
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_income - total_expense

    # ✅ Step 2: Recent Transactions
    recent_transactions = transactions.order_by('-date')[:5]

    # ✅ ⭐ Step 4: Chart Data (ADD HERE)
    category_data = transactions.filter(type='expense') \
        .values('category__name') \
        .annotate(total=Sum('amount'))

    labels = [item['category__name'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    # ✅ Final context
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }

    return render(request, 'home.html', context)
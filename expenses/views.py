from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout

from .models import Expense
from .forms import ExpenseForm



def is_admin(user):
    return user.is_authenticated and user.is_staff



def index(request):
    if request.user.is_authenticated:
        return redirect('expense_list')
    return render(request, 'expenses/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('expense_list')
        else:
            return render(request, 'expenses/index.html', {'error': 'Invalid username/password.'})
    return render(request, 'expenses/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@user_passes_test(is_admin, login_url='index')
def expense_list(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    expenses = Expense.objects.all()
    if query:
        expenses = expenses.filter(category__icontains=query)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    total = sum(exp.amount for exp in expenses)

    category_totals = (
        expenses.values('category')
        .annotate(total_amount=Sum('amount'))
        .order_by('-total_amount')
    )

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'total': total,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'category_totals': list(category_totals),
    })


@user_passes_test(is_admin, login_url='index')
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})


@user_passes_test(is_admin, login_url='index')
def edit_expense(request, id):
    expense = Expense.objects.get(id=id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})


@user_passes_test(is_admin, login_url='index')
def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    return redirect('expense_list')

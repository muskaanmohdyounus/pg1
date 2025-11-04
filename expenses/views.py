from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
import random
from .models import Expense, OTP, ManagerProfile
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ManagerOnboarding




def is_admin(user):
    """Check if the user is an authenticated admin (staff)."""
    return user.is_authenticated and user.is_staff




def index(request):
    """Homepage — ALWAYS show index. No redirects."""
    return render(request, 'expenses/index.html')


def login_view(request):
    """Handle login authentication."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('expense_list')
        else:
            return render(request, 'expenses/login.html', {
                'error': 'Invalid username or password.'
            })
    return render(request, 'expenses/login.html')


@login_required
def logout_view(request):
    """Logout and redirect to homepage."""
    logout(request)
    return redirect('index')


def signup(request):
    if request.method == "POST":

        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        pg_property = request.POST.get("pg_property")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        otp_entered = request.POST.get("otp")

        otp_record = OTP.objects.filter(phone=phone).order_by("-created_at").first()

        print("OTP ENTERED:", otp_entered)
        print("OTP RECORD:", otp_record)
        print("PASSWORDS:", password, confirm_password)
        print("USERNAME EXISTS:", User.objects.filter(username=username).exists())
        print("EMAIL EXISTS:", User.objects.filter(email=email).exists())

        if not otp_record or otp_record.otp_code != otp_entered:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, "expenses/signup.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "expenses/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "expenses/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "expenses/signup.html")

       
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

       
        ManagerProfile.objects.create(
            user=user,
            full_name=full_name,
            phone=phone,
            pg_property=pg_property
        )

        from django.contrib.auth import login
        login(request, user)

       
        return redirect("onboarding")

    return render(request, "expenses/signup.html")



def onboarding_view(request):
    onboarding, created = ManagerOnboarding.objects.get_or_create(user=request.user)

   
    questions = [
        "How many PG properties do you manage?",
        "How many total rooms are there?",
        "How many tenants are currently staying?",
        "Do you have staff? (Yes/No)",
        "What is your biggest challenge in managing the PG?"
    ]

    
    answers = [
        onboarding.answer1 or "",
        onboarding.answer2 or "",
        onboarding.answer3 or "",
        onboarding.answer4 or "",
        onboarding.answer5 or "",
    ]

    
    try:
        step = answers.index("")
    except ValueError:
       
        logout(request)
        return redirect('login')

   
    if request.method == "POST":
        ans = request.POST.get('answer')

        if step == 0:
            onboarding.answer1 = ans
        elif step == 1:
            onboarding.answer2 = ans
        elif step == 2:
            onboarding.answer3 = ans
        elif step == 3:
            onboarding.answer4 = ans
        elif step == 4:
            onboarding.answer5 = ans

        onboarding.save()

        return redirect('onboarding') 

    
    context = {
        'question': questions[step],
        'step': step + 1,
    }

    return render(request, 'expenses/onboarding.html', context)



@login_required
def expense_list(request):
    """Display and filter all expenses with total and chart data."""
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    expenses = Expense.objects.all().order_by('-date')

   
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
        'category_totals_json': list(category_totals),
    })




@user_passes_test(is_admin, login_url='index')
def add_expense(request):
    """Add a new expense record."""
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')
        description = request.POST.get('description')
        bill_image = request.FILES.get('bill_image')

        
        Expense.objects.create(
            title=title,
            amount=amount,
            category=category,
            date=date,
            description=description,
            bill_image=bill_image
        )
        return redirect('expense_list')

    return render(request, 'expenses/add_expense.html')




@user_passes_test(is_admin, login_url='index')
def edit_expense(request, id):
    """Edit an existing expense record."""
    expense = get_object_or_404(Expense, id=id)

    if request.method == 'POST':
        expense.title = request.POST.get('title')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')
        expense.description = request.POST.get('description')

        # Update bill image only if new one is uploaded
        if request.FILES.get('bill_image'):
            expense.bill_image = request.FILES.get('bill_image')

        expense.save()
        return redirect('expense_list')

    return render(request, 'expenses/edit_expense.html', {'expense': expense})




@user_passes_test(is_admin, login_url='index')
def delete_expense(request, id):
    """Delete an expense record."""
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')

@user_passes_test(is_admin, login_url='index')
def settings_page(request):
    """Display Settings page."""
    return render(request, 'expenses/settings.html')

def reports_page(request):
    
    monthly_data = (
        Expense.objects
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('-month')
    )

   
    monthly_reports = []
    for data in monthly_data:
        month = data['month']
        total = data['total']
        top_category = (
            Expense.objects.filter(date__month=month.month)
            .values('category')
            .annotate(total_category=Sum('amount'))
            .order_by('-total_category')
            .first()
        )
        monthly_reports.append({
            'month': month.strftime('%B %Y'),
            'total': total,
            'top_category': top_category['category'] if top_category else 'N/A',
            'top_category_total': top_category['total_category'] if top_category else 0
        })

    return render(request, 'expenses/reports.html', {'monthly_reports': monthly_reports})

def send_otp(request):
    phone = request.GET.get("phone")

    if not phone:
        return JsonResponse({"status": "error", "message": "Phone number required"})

    otp_code = str(random.randint(1000, 9999))

    
    OTP.objects.create(phone=phone, otp_code=otp_code)

    
    print("===================================")
    print(f"OTP for {phone} → {otp_code}")
    print("===================================")

    return JsonResponse({"status": "success", "message": "OTP sent"})
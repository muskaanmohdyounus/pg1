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



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense

from .models import Property

@login_required
def expense_list(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    expenses = Expense.objects.all().order_by('-entry_date')

    if query:
        expenses = expenses.filter(category__name__icontains=query)
    if start_date:
        expenses = expenses.filter(entry_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(entry_date__lte=end_date)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # Summary by category
    summary_categories = ['Utility', 'Food', 'Staff', 'Miscellaneous']
    category_summary = {}
    for cat_name in summary_categories:
        amt = expenses.filter(category__name__icontains=cat_name).aggregate(Sum('amount'))['amount__sum'] or 0
        category_summary[cat_name] = amt

    # Highest single expense
    highest_expense = expenses.order_by('-amount').first()

    # Category chart data
    category_totals = expenses.values('category__name').annotate(total_amount=Sum('amount')).order_by('-total_amount')
    chart_labels = [item['category__name'] or 'Uncategorized' for item in category_totals]
    chart_values = [item['total_amount'] for item in category_totals]

    # ✅ Fetch all properties for filter dropdown
    properties = Property.objects.all()

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'total': total,
        'category_summary': category_summary,
        'highest_expense': highest_expense,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'properties': properties,  # <--- added
    })

@login_required
def expense_detail(request, id):
    expense = get_object_or_404(Expense, id=id)
    return render(request, 'expenses/expense_detail.html', {
        'expense': expense
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Expense, Category, Property

# Use a lambda directly instead of missing is_admin
@user_passes_test(lambda u: u.is_staff, login_url='index')
def add_expense(request):
    categories = Category.objects.all()
    properties = Property.objects.all()

    if request.method == "POST":
        property_id = request.POST.get("property")
        category_name = request.POST.get("category", "").strip()  # manual input
        sub_category = request.POST.get("sub_category", "").strip()
        amount = request.POST.get("amount")
        entry_date = request.POST.get("entry_date")
        description = request.POST.get("description", "").strip()
        bill_image = request.FILES.get("bill_image")

        # Validate required fields
        if not property_id or not amount or not entry_date:
            messages.error(request, "Please fill all required fields.")
            return redirect("expenses:add")

        # Get Property object safely
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            messages.error(request, "Invalid Property selected.")
            return redirect("expenses:add")

        # Get or create Category by name (manual input)
        cat = None
        if category_name:
            cat, created = Category.objects.get_or_create(name=category_name)

        # Create Expense
        Expense.objects.create(
            property=prop,
            category=cat,
            sub_category=sub_category,
            amount=amount,
            entry_date=entry_date,
            description=description,
            bill_image=bill_image
        )

        messages.success(request, "Expense added successfully!")
        return redirect("expense_list")


    context = {
        "categories": categories,
        "properties": properties
    }
    return render(request, "expenses/add_expense.html", context)



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Property, Category

@login_required
def edit_expense(request, id):
    """Edit an existing expense record."""
    expense = get_object_or_404(Expense, id=id)
    
    categories = Category.objects.all()
    properties = Property.objects.all()

    if request.method == 'POST':
        # Basic fields
        expense.amount = request.POST.get('amount')
        expense.description = request.POST.get('description')
        expense.entry_date = request.POST.get('entry_date')
        expense.sub_category = request.POST.get('sub_category', '')

        # ForeignKeys
        category_id = request.POST.get('category')
        if category_id:
            expense.category = Category.objects.get(id=category_id)
        else:
            expense.category = None

        property_id = request.POST.get('property')
        if property_id:
            expense.property = Property.objects.get(id=property_id)
        else:
            expense.property = None

        # Optional fields
        expense.paid_by = request.POST.get('paid_by', '')
        expense.paid_to = request.POST.get('paid_to', '')
        paid_mode = request.POST.get('paid_mode')
        if paid_mode in dict(Expense.PAYMENT_MODES).keys():
            expense.paid_mode = paid_mode
        else:
            expense.paid_mode = 'Cash'  # default fallback

        # Bill image (only update if new file uploaded)
        if request.FILES.get('bill_image'):
            expense.bill_image = request.FILES.get('bill_image')

        expense.save()
        messages.success(request, "Expense updated successfully!")
        return redirect('expense_list')

    return render(request, 'expenses/edit_expense.html', {
        'expense': expense,
        'categories': categories,
        'properties': properties,
    })




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



from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Property
from .forms import PropertyForm
from .models import PropertyImage



# ✅ 1. PROPERTY LIST — shows all properties
def property_list(request):
    properties = Property.objects.all().order_by('-id')
    return render(request, 'expenses/property_list.html', {
        'properties': properties
    })


# ✅ 2. ADD NEW PROPERTY
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        files = request.FILES.getlist('images')

        if form.is_valid():
            property_obj = form.save()

            # Save uploaded images
            for file in files:
                PropertyImage.objects.create(property=property_obj, image=file)

            return redirect('property_list')
    else:
        form = PropertyForm()

    return render(request, 'expenses/add_property.html', {
        'form': form
    })



# ✅ 3. PROPERTY DETAIL PAGE
def property_detail(request, id):
    property_obj = get_object_or_404(Property, id=id)
    return render(request, 'expenses/property_detail.html', {
        'property': property_obj
    })


# ✅ 4. EDIT PROPERTY
def edit_property(request, id):
    property_obj = get_object_or_404(Property, id=id)

    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        files = request.FILES.getlist('images')

        if form.is_valid():
            form.save()

            # Add new images
            for file in files:
                PropertyImage.objects.create(property=property_obj, image=file)

            return redirect('property_detail', id=id)

    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'expenses/edit_property.html', {
        'form': form,
        'property': property_obj,
        'images': property_obj.images.all()
    })



# ✅ 5. DELETE PROPERTY
def delete_property(request, id):
    property_obj = get_object_or_404(Property, id=id)

    if request.method == 'POST':
        property_obj.delete()
        return redirect('property_list')

    return render(request, 'expenses/delete_confirm.html', {
        'property': property_obj
    })

import json
from collections import Counter
from django.shortcuts import render
from .models import Property

def property_graph(request):
    properties = Property.objects.all()

    # Chart 1: Occupancy per property
    property_names = [p.name for p in properties]
    occupancy = [p.occupancy_percent for p in properties]

    # Chart 2: Property type distribution
    types = [p.type for p in properties]
    type_counts = dict(Counter(types))

    # Chart 3: Occupied vs Vacant beds
    occupied_beds = [p.occupied_beds for p in properties]
    vacant_beds = [p.vacant_beds for p in properties]

    context = {
        'property_names': json.dumps(property_names),
        'occupancy': json.dumps(occupancy),
        'type_labels': json.dumps(list(type_counts.keys())),
        'type_counts': json.dumps(list(type_counts.values())),
        'occupied_beds': json.dumps(occupied_beds),
        'vacant_beds': json.dumps(vacant_beds),
    }

    return render(request, 'expenses/property_graph.html', context)

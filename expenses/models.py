from django.db import models
from django.contrib.auth.models import User


# ---------------------------
# Property Models (Do not touch)
# ---------------------------
class Property(models.Model):
    PROPERTY_TYPES = (
        ('Student Living', 'Student Living'),
        ('Mix', 'Mix'),
        ('PG', 'PG'),
    )

    TENANT_TYPES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Any', 'Any'),
    )

    STATUS_CHOICES = (
        ('Live', 'Live'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    tenant_type = models.CharField(max_length=20, choices=TENANT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    address = models.TextField()
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, blank=True, null=True)

    total_beds = models.PositiveIntegerField(default=0)
    occupied_beds = models.PositiveIntegerField(default=0)
    rent_per_bed = models.PositiveIntegerField(default=0, blank=True, null=True)

    amenities = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def vacant_beds(self):
        return self.total_beds - self.occupied_beds if self.total_beds >= self.occupied_beds else 0

    @property
    def occupancy_percent(self):
        if self.total_beds == 0:
            return 0
        return round((self.occupied_beds / self.total_beds) * 100)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="property_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.name}"

# ---------------------------
# Category Model
# ---------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ---------------------------
# Expense Model
# ---------------------------
from django.db import models
from .models import Property, Category  # adjust import if needed

class Expense(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True, blank=True
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    sub_category = models.CharField(max_length=100, blank=True)  # NEW FIELD

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    description = models.TextField(blank=True)
    bill_image = models.ImageField(upload_to='bills/', blank=True, null=True)

    # NEW FIELDS
    paid_by = models.CharField(max_length=100, blank=True, null=True)
    paid_to = models.CharField(max_length=100, blank=True, null=True)
    
    PAYMENT_MODES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Other', 'Other'),
    ]
    paid_mode = models.CharField(max_length=20, choices=PAYMENT_MODES, default='Cash')

    def __str__(self):
        prop_name = self.property.name if self.property else "No Property"
        cat_name = self.category.name if self.category else "No Category"
        sub_cat_name = self.sub_category if self.sub_category else "No Subcategory"
        return f"{prop_name} - {cat_name} - {sub_cat_name} - ₹{self.amount}"

# ---------------------------
# Other Models (Manager & OTP)
# ---------------------------
class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    pg_property = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"

class OTP(models.Model):
    phone = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.otp_code}"

class ManagerOnboarding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    answer1 = models.CharField(max_length=255, blank=True)
    answer2 = models.CharField(max_length=255, blank=True)
    answer3 = models.CharField(max_length=255, blank=True)
    answer4 = models.CharField(max_length=255, blank=True)
    answer5 = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Onboarding - {self.user.username}"





from django.db import models
from django.utils import timezone

class Loan(models.Model):
    # Status Choices
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_DISBURSED = 'disbursed'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_DISBURSED, 'Disbursed'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    # Tenant details (NO FOREIGN KEY NOW)
    tenant_name = models.CharField(max_length=255)
    tenant_id = models.CharField(max_length=100)
    room_number = models.CharField(max_length=50, blank=True, null=True)

    # Tenant-supplied fields
    loan_amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    loan_purpose = models.CharField(max_length=255)
    loan_type = models.CharField(max_length=100, blank=True, null=True)
    repayment_months = models.PositiveIntegerField(default=1)
    document = models.FileField(upload_to='loan_docs/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # Admin fields (owner updates these)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    # Auto timestamps
    applied_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Calculated field
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-applied_date']

    def __str__(self):
        return f"Loan #{self.pk} - {self.tenant_name} - {self.status}"

    def calc_installment_source_amount(self):
        # EMI uses approved_amount if exists, else requested amount
        return self.approved_amount if self.approved_amount else self.loan_amount_requested

    def calculate_monthly_installment(self):
        source_amount = self.calc_installment_source_amount() or 0
        months = self.repayment_months or 1
        try:
            return round(source_amount / months, 2)
        except:
            return 0

    def save(self, *args, **kwargs):
        # Recalculate EMI on every save
        self.monthly_installment = self.calculate_monthly_installment()
        super().save(*args, **kwargs)


class Tenant(models.Model):
    tenant_name = models.CharField(max_length=100)
    tenant_phone = models.CharField(max_length=15)
    tenant_email = models.EmailField(unique=True)
    property_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.tenant_name

class OwnerTenant(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Activation'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
    ]

    tenant_property = models.ForeignKey(
        'Property', 
        on_delete=models.CASCADE, 
        related_name='owner_tenants',
        verbose_name='Property'
    )
    tenant_unique_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    guardian_name = models.CharField(max_length=255, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    room_number = models.CharField(max_length=50)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    move_in_date = models.DateField(blank=True, null=True)
    stay_duration_months = models.PositiveIntegerField(default=12)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated_at = models.DateTimeField(blank=True, null=True)
    is_signup_allowed = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.tenant_unique_id:
            last = OwnerTenant.objects.all().order_by('id').last()
            if last:
                last_id = int(last.tenant_unique_id.replace("TEN", ""))
                self.tenant_unique_id = f"TEN{last_id + 1:03d}"
            else:
                self.tenant_unique_id = "TEN001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"



class TenantKYC(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    tenant = models.OneToOneField(OwnerTenant, on_delete=models.CASCADE, related_name='kyc')
    full_name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    id_type = models.CharField(max_length=100)
    id_number = models.CharField(max_length=100)
    id_document = models.FileField(upload_to='kyc_documents/')
    selfie = models.ImageField(upload_to='kyc_selfies/')
    address = models.TextField()
    permanent_address = models.TextField()
    emergency_contact = models.CharField(max_length=50)
    occupation = models.CharField(max_length=100)
    kyc_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')

    def __str__(self):
        return f"KYC - {self.tenant.name}"

import uuid
from django.db import models



class OwnerRent(models.Model):
    # Linking to existing models
    tenant = models.ForeignKey('OwnerTenant', on_delete=models.CASCADE, related_name='rents')
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='rents')

    room_number = models.CharField(max_length=20)  # Auto-filled from tenant

    # Room Sharing
    ROOM_SHARING_CHOICES = (
        ("1-sharing", "Single Sharing"),
        ("2-sharing", "Double Sharing"),
        ("3-sharing", "Triple Sharing"),
    )
    room_sharing = models.CharField(max_length=10, choices=ROOM_SHARING_CHOICES, default="1-sharing")

    # Billing Information
    billing_month = models.CharField(max_length=20)  # January, February...
    billing_year = models.IntegerField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment
    PAYMENT_METHODS = (
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("NetBanking", "NetBanking"),
        ("Wallet", "Wallet"),
        ("Cash", "Cash"),
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
    )
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")

    # Proof of payment
    utr_number = models.CharField(max_length=100, blank=True, null=True)
    bill_upload = models.FileField(upload_to="owner_rent_bills/", blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Auto-generate unique rent ID
    rent_id = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.rent_id:
            self.rent_id = str(uuid.uuid4()).split("-")[0].upper()
        if not self.room_number and self.tenant:
            self.room_number = self.tenant.room_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tenant.name} - {self.billing_month} {self.billing_year}"




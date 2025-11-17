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

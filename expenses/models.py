from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Electricity', 'Electricity'),
        ('Groceries', 'Groceries'),
        ('Maintenance', 'Maintenance'),
        ('Salary', 'Salary'),
        ('Misc', 'Miscellaneous'),
    ]

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    bill_image = models.ImageField(upload_to='bills/', blank=True, null=True)
    

    def __str__(self):
        return f"{self.title} - {self.amount}"

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

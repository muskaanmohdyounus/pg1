from django import forms
from .models import Expense, Property, PropertyImage, Loan, OwnerTenant, Tenant, TenantKYC

# ---------------------------
# EXPENSE FORM
# ---------------------------
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'entry_date', 'description', 'bill_image']

# ---------------------------
# PROPERTY FORMS
# ---------------------------
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

# ---------------------------
# LOAN FORM
# ---------------------------
class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        # Exclude admin & tenant linkage fields, set in views
        exclude = [
            'tenant_name', 'tenant_id', 'room_number',
            'approved_amount', 'approved_date', 'admin_notes',
            'status', 'monthly_installment', 'applied_date', 'updated_at'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows':3}),
            'loan_purpose': forms.TextInput(),
            'loan_type': forms.TextInput(),
        }

    def clean_repayment_months(self):
        months = self.cleaned_data.get('repayment_months')
        if not months or months < 1:
            raise forms.ValidationError("Repayment months must be at least 1.")
        return months

# ---------------------------
# OWNER TENANT FORM
# ---------------------------
class OwnerTenantForm(forms.ModelForm):
    class Meta:
        model = OwnerTenant
        fields = [
            'tenant_property',
            'name',
            'email',
            'phone',
            'room_number',
            'rent_amount',
            'move_in_date',
            'stay_duration_months',
        ]
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = OwnerTenant
        exclude = ['status', 'tenant_unique_id']  # exclude status
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Guardian Name'}),
            'guardian_phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Guardian Phone', 'maxlength':'10'}),
            'tenant_property': forms.Select(attrs={'class':'form-select'}),
            'room_number': forms.TextInput(attrs={'class':'form-control'}),
            'move_in_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'stay_duration_months': forms.NumberInput(attrs={'class':'form-control'}),
            'rent_amount': forms.NumberInput(attrs={'class':'form-control'}),
            'notes': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

    def clean_guardian_phone(self):
        phone = self.cleaned_data.get('guardian_phone')
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError("Guardian phone must be exactly 10 digits.")
        return phone



# ---------------------------
# TENANT KYC FORMS
# ---------------------------
class TenantKYCDetailsForm(forms.ModelForm):
    """Full tenant KYC details for admin/owner view"""
    class Meta:
        model = TenantKYC
        fields = [
            'full_name',
            'dob',
            'id_type',
            'id_number',
            'id_document',
            'selfie',
            'address',
            'permanent_address',
            'emergency_contact',
            'occupation',
            'kyc_status',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_type': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'id_document': forms.FileInput(attrs={'class': 'form-control'}),
            'selfie': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'kyc_status': forms.Select(attrs={'class': 'form-select'}),
        }
class TenantKYCUploadForm(forms.ModelForm):
    """Form for tenant to upload KYC documents"""
    class Meta:
        model = TenantKYC
        fields = ['id_document', 'selfie']
        widgets = {
            'id_document': forms.FileInput(attrs={'class': 'form-control'}),
            'selfie': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # No strict validation for now
        return cleaned_data

class TenantKYCTenantForm(forms.ModelForm):
    """Tenant full KYC submission form"""
    class Meta:
        model = TenantKYC
        fields = [
            'full_name',
            'dob',
            'id_type',
            'id_number',
            'id_document',
            'selfie',
            'address',
            'permanent_address',
            'emergency_contact',
            'occupation',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_type': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'id_document': forms.FileInput(attrs={'class': 'form-control'}),
            'selfie': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import OwnerTenant

MONTH_CHOICES = [
    ("January", "January"), ("February", "February"), ("March", "March"),
    ("April", "April"), ("May", "May"), ("June", "June"),
    ("July", "July"), ("August", "August"), ("September", "September"),
    ("October", "October"), ("November", "November"), ("December", "December"),
]

YEAR_CHOICES = [(y, y) for y in range(2023, 2031)]  # adjust range as needed

ROOM_SHARING_CHOICES = [
    ("single", "Single Sharing"),
    ("double", "2 Sharing"),
    ("triple", "3 Sharing"),
]

class OwnerRentCreateForm(forms.Form):
    tenant = forms.ModelChoiceField(
        queryset=OwnerTenant.objects.all(),
        empty_label="Select Tenant",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    billing_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    billing_year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    room_sharing = forms.ChoiceField(
        choices=ROOM_SHARING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    rent_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Rent Amount'})
    )
    due_date = forms.DateField(
        required=False,  # optional
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
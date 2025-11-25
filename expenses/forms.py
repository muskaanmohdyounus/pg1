from django import forms

from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'entry_date', 'description', 'bill_image']


from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
 
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

from django import forms
from .models import Loan

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        # exclude admin fields and tenant linkage fields - set in view
        exclude = [ 'tenant_name', 'tenant_id', 'room_number', 'approved_amount', 'approved_date', 'admin_notes', 'status', 'monthly_installment', 'applied_date', 'updated_at']
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

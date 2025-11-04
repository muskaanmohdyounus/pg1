from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description','bill_image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}),
        }

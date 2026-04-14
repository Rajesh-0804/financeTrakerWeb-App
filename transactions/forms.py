from django import forms
from transactions.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
    'amount': forms.NumberInput(attrs={'class': 'form-control'}),
    'type': forms.Select(attrs={'class': 'form-control'}),
    'category': forms.Select(attrs={'class': 'form-control'}),
    'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    'description': forms.Textarea(attrs={'class': 'form-control'}),
}
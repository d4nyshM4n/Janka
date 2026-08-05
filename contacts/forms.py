from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'eco-input',
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'eco-input',
                'placeholder': 'Ваш Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'eco-input',
                'placeholder': 'Телефон (необязательно)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'eco-input eco-textarea',
                'placeholder': 'Ваше сообщение или отзыв...',
                'rows': 4
            }),
        }
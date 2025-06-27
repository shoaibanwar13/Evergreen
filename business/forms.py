# ============================================
# FORMS.PY
# ============================================

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User


class CustomUserSignupForm(UserCreationForm):
    """Custom signup form with additional fields"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Enter First Name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Enter Last Name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Enter Email Address'
        })
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': '+1234567890'
        })
    )
    
    company_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Enter Company Name'
        })
    )
    
    license_no = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Enter License Number'
        })
    )
    
    business_logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'border-0 px-3 py-3 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'accept': 'image/*'
        })
    )
    
    document = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'border-0 px-3 py-3 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'accept': '.pdf,.doc,.docx'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 
                 'company_name', 'license_no', 'business_logo', 'document', 
                 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Choose Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Enter Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'border-0 px-3 py-3 placeholder-gray-400 text-black bg-white rounded text-sm shadow focus:outline-none focus:ring w-full ease-linear transition-all duration-150',
            'placeholder': 'Confirm Password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.license_no = self.cleaned_data['license_no']
        user.business_logo = self.cleaned_data.get('business_logo')
        user.document = self.cleaned_data.get('document')
        
        if commit:
            user.save()
        return user


 

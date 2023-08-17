from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UserCreationForm(forms.ModelForm):
    phone = PhoneNumberField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password', 'phone')


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all_'

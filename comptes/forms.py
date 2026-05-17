from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Adresse Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'photo', 'interests']
        widgets = {
            'interests': forms.CheckboxSelectMultiple(),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

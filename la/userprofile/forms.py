from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


INPUT_CLASS = 'w-full my-4 py-4 px-6 rounded-xl bg-gray-100'

username="Nombre de usuario"
class LoginForm(AuthenticationForm):
    
    username = forms.CharField(label="Nombre de Usuario", widget=forms.TextInput(attrs={
        
        'placeholder': 'Ingrese su usuario',
        'class': INPUT_CLASS
        
    })) 
    
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese su contraseña',
        'class': INPUT_CLASS
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(label="Nombre de usuario",widget=forms.TextInput(attrs={
        'placeholder': 'Escriba su nuevo usuario',
        'class': INPUT_CLASS
    }))
    email = forms.CharField(label="Correo electronico",widget=forms.EmailInput(attrs={
        'placeholder': 'Ingrese su correo',
        'class': INPUT_CLASS
    }))
    password1 = forms.CharField(label="Constraseña", widget=forms.PasswordInput(attrs={
        'placeholder': 'Escriba su contraseña',
        'class': INPUT_CLASS
    }))
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita la contraseña',
        'class': INPUT_CLASS
    }))
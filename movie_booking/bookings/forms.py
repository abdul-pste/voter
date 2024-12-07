from django import forms
from .models import User, Movie, Showtime, Booking
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Render password input as a password field
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Use your custom User model here
        fields = ('email', 'password1', 'password2')

class MovieSearchForm(forms.Form):
    q = forms.CharField(label='Movie Title', max_length=100, required=True)
    location = forms.CharField(label='Location', max_length=100, required=True)


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title']


class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = ['date', 'time', 'cinema_hall']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["tickets"]  # Add other fields as needed
        widgets = {
            "tickets": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Render password input as masked
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
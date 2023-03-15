from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SurfSpot
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class SurfSpotForm(forms.ModelForm):
    class Meta:
        model = SurfSpot
        fields = ('name', 'description', 'country', 'continent', 'best_wind', 'wave_direction', 'spot_type',
                  'wave_type', 'swell_size', 'crowd', 'difficulty', 'danger', 'latitude', 'longitude')

        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'validate', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


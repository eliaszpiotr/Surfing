from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, SurfSpot, UserProfile


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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['country', 'bio', 'home_spot', 'profile_picture']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'home_spot': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'})
        }

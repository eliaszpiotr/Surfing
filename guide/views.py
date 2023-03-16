from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, SurfSpotForm, UserProfileForm
from .models import SurfSpot


class HomeView(View):

    def get(self, request):
        return render(request, 'guide/base.html')


class SpotsListView(ListView):
    model = SurfSpot
    template_name = 'guide/spots_list.html'
    context_object_name = 'spots'
    ordering = ['name']
    paginate_by = 10


class RegisterView(FormView):
    template_name = 'guide/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_profile_form')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{form.fields[field].label}: {error}")
        return super().form_invalid(form)


class UserProfileFormView(FormView):
    template_name = 'guide/user_profile_form.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user_profile = form.save(commit=False)
        user_profile.user = self.request.user
        user_profile.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'guide/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        return reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Incorrect username or password.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class CreateSurfSpotView(CreateView):
    model = SurfSpot
    form_class = SurfSpotForm
    template_name = 'guide/create_surf_spot.htm'
    success_url = reverse_lazy('home')

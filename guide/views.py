from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm, SurfSpotForm, LoginForm
from .models import SurfSpot, CustomUser


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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
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


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class CreateSurfSpotView(CreateView):
    model = SurfSpot
    form_class = SurfSpotForm
    template_name = 'guide/create_surf_spot.htm'
    success_url = reverse_lazy('home')

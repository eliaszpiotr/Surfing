from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect

from .forms import CustomUserCreationForm, SurfSpotForm, LoginForm
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


class LoginRegisterView(TemplateView):
    template_name = 'guide/login_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['register_form'] = CustomUserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'login' in request.POST:
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('home'))
        elif 'register' in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse_lazy('home'))

        return self.render_to_response(self.get_context_data())


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class CreateSurfSpotView(CreateView):
    model = SurfSpot
    form_class = SurfSpotForm
    template_name = 'guide/create_surf_spot.htm'
    success_url = reverse_lazy('home')

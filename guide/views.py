from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm


class HomeView(View):
    def get(self, request):
        return render(request, 'guide/home.html')


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'guide/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

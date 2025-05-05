# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.shortcuts import render

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    

def discover(request):
    dummy_items = range(6)  # This gives you 5 items
    return render(request, 'discover.html', {'range': dummy_items})



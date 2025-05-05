# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.http import JsonResponse
from RecommendationEngine import placeholder_db
from django.shortcuts import render

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def get_devs(request):
    #API returns all developers in db in a json format
    try:
        devs = placeholder_db.fetchAllDevelopers()
        return JsonResponse({'developers': devs})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
def add_dev(request):
    #API to add a new developer
    if request.method == "POST":
        dev_name = request.POST.get("devName")
        if dev_name:
            try:
                placeholder_db.createDeveloper([dev_name])
                return JsonResponse({"message": "Developer added"}, status=201)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        return JsonResponse({"error": "Invalid request"}, status=400)

def discover(request):
    dummy_items = range(5)  # This gives you 5 items
    return render(request, 'discover.html', {'range': dummy_items})

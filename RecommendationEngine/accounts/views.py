# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.http import JsonResponse
from RecommendationEngine import placeholder_db

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def get_devs(request):
    #API returns all developers in db in a json format
    try:
        db_path = "placeholder.db"
        con, cur = placeholder_db.makeConnection(db_path)
        devs = placeholder_db.fetchAllDevelopers(cur)
        con.close()
        return JsonResponse({'developers': devs})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def add_dev(request):

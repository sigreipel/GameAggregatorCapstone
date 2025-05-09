# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render
from .models import CustomUser
from .forms import CustomUserCreationForm
from RecommendationEngine import placeholder_db
import json
import os
import random


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
    query = request.GET.get('query', '').lower()

    # Load the JSON data from file
    base_dir = os.path.dirname(os.path.abspath(__file__))  # adjust if needed
    json_path = os.path.join(base_dir, 'data/articles.json')

    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    articles = data.get("articles", [])

    # Filter articles if there's a search query
    if query:
        articles = [
            article for article in articles
            if query in article.get("title", "").lower() or query in article.get("description", "").lower()
        ]

    # Pass 'articles' and 'query' into the template context
    return render(request, 'discover.html', {
        'articles': articles,
        'query': query
    })
    
def home_view(request):
    # Load the JSON data from file
    base_dir = os.path.dirname(os.path.abspath(__file__))  # adjust if needed
    json_path = os.path.join(base_dir, 'data/articles.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    articles = data.get('articles', [])
    article = random.choice(articles) if articles else None
    return render(request, 'home.html', {'article': article})

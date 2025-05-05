# accounts/urls.py
from django.urls import path

from .views import SignUpView, get_devs, add_dev
from django.views.generic import TemplateView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dev_list/", TemplateView.as_view(template_name="list_devs.html"), name="dev_list"),
    path("add_devs/", add_dev, name="add_dev"),
    path("dev_form/", TemplateView.as_view(template_name="add_dev.html"), name="dev_form")
]
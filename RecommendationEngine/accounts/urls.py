# accounts/urls.py
from django.urls import path

from .views import SignUpView, get_devs, add_dev


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("devs/", get_devs, name="get_devs"),
    path("add_devs/", add_dev, name="add_dev")
]
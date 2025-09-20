from django.urls import path
from .import views


urlpatterns = [
    path('', views.UserRegitration.as_view(), name='registration'),
    path("login", views.LoginView.as_view(), name="login"),

]

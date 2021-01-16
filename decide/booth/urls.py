from django.urls import path
from .views import BoothView
from . import views

urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('login/', views.loginPage, name="login"),
    path('', views.welcome, name="welcome"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('prueba/', views.prueba, name="prueba"),
    path('about/', views.about, name="about"),
]

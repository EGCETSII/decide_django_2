from django.urls import path
from .views import BoothView
from . import views

urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view(), name="booth"),
    path('login/', views.loginPage, name="login"),
    path('', views.welcome, name="welcome"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('hasVotado/', views.hasVotado, name="hasVotado"),
    path('peticionCenso/', views.peticionCensoUsuario, name="peticionCensoUsuario"),
    path('peticionCensoAdmin/', views.peticionCensoAdmin, name="peticionCensoAdmin"),
    path('deletePeticion/<str:pk>/', views.deletePeticion, name="deletePeticion"),
    path('about/', views.about, name="about"),
]

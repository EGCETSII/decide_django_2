from django.urls import path
from .views import BoothView
from django.views.generic import TemplateView


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
]

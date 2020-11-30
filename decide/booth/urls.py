from django.urls import path
from .views import BoothView
from django.views.generic import TemplateView


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('', TemplateView.as_view(template_name='index.html'))
]

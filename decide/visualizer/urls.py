from django.urls import path, include
from .views import VisualizerView
from django.conf.urls import url

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    url('i18n/', include('django.conf.urls.i18n')),
]


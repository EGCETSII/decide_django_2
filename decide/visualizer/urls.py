from django.urls import path, include
from .views import VisualizerView, AboutUs, ContactUs, VisualizerHome
from django.conf.urls import url

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('contactUs/', ContactUs.as_view()),
    path('aboutUs/', AboutUs.as_view()),
    path('', VisualizerHome.as_view()),
    url('i18n/', include('django.conf.urls.i18n')),
]


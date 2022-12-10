from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census'),
]

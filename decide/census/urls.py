from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('votings/<int:voter_id>/', views.ListVotingsByVoter.as_view(), name='census_votings'),
]

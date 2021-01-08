from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('votacionBinaria/<id>/', views.getVotacionBinariaById, name='Votacion Binaria'),
    path('votacion/<id>/', views.getVotacionById, name='Votacion'),
    path('votacionMultiple/<id>/', views.getVotacionMultipleById, name='Votacion Multiple'),
    path('votacionPreferencia/<id>/', views.getVotacionPreferenciaById, name='Votacion Preferencia')
]

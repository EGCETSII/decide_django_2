from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),

    path('votacionBinaria/<id>/', views.getVotacionBinariaById, name='Votacion Binaria'),
    path('votacionBinaria/all', views.getAllVotacionesBinarias, name='Votacion Binaria Todas'),

    path('votacion/<id>/', views.getVotacionById, name='Votacion'),
    path('votacion/all', views.getAllVotaciones, name='Votacion Todas'),

    path('votacionMultiple/<id>/', views.getVotacionMultipleById, name='Votacion Multiple'),
    path('votacionMultiple/all', views.getAllVotacionesMultiples, name='Votacion Multiple Todas'),

    path('votacionPreferencia/<id>/', views.getVotacionPreferenciaById, name='Votacion Preferencia'),
    path('votacionPreferencia/all', views.getAllVotacionesPreferencia, name='Votacion Preferencia')
]

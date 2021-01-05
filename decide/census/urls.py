from django.urls import path, include
from . import views
from census.views import importCensusFromLdap, main_census

urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    #Añadir a partir de aqui
    path('addLDAPcensus', importCensusFromLdap, name='addLDAPcensus'),
]


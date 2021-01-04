from django.urls import path, include
from . import views
from census.views import importCensusFromLdap

urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    #Añadir a partir de aqui
    path('addLDAPcensus', importCensusFromLdap, name='addLDAPcensus'),
    path('main_census', views.main_census, name='main_census'),
]

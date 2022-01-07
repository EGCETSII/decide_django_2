from django.urls import path
from . import views
from .views import GroupsView


urlpatterns = [
     path('', views.CensusCreate.as_view(), name='census_create'),
     path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
     path('union', views.GroupOperationsAPI.as_view(), name='group_union'),
     path('intersection', views.GroupOperationsAPI.as_view(),
         name='group_intersection'),
     path('difference', views.GroupOperationsAPI.as_view(),
         name='group_difference'),
     path('operations/', views.GroupOperations.as_view(),
         name='group_operations'),
     path('groups/import/', views.ImportExportGroup.importGroup),
     path('groups/export/', views.ImportExportGroup.exportGroup),
     path('groupList', GroupsView.as_view()),
     path('joinGroup/', views.joinGroup.as_view()),

]

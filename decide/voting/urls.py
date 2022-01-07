from django.urls import path
from . import views
from voting.views import *


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('notifications_admin/', voting_admin_notification),
    path('notifications/', voting_user_notification),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
]

from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import include, path
from django.contrib.auth import views as auth_views

from .views import GetUserView, LogoutView, RegisterView, RegisterGUI, LogOutTestView, AccountActivation, ProfileView, UserProfile, EditUserProfile, EditProfileView, DeleteProfile, DeleteProfileView


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('editprofile/', EditProfileView.as_view()),
    path('deleteprofile/', DeleteProfileView.as_view()),
    #Register URL
    path('registergui/', RegisterGUI.register, name='account_activation_sent'),
    #Login URL Built In
    path('logingui/', auth_views.login,{'template_name': 'login.html'}, name='login2'),
    #Logout URL
    path('logoutgui/', LogOutTestView.logout, name='logout'),
    #Account activation sent view
    path(r'^account_activation_sent/$', AccountActivation.account_activation_sent, name='account_activation_sent'),
    #Activation URL
    path('activate/<slug:uidb64>/<slug:token>/', AccountActivation.activate, name='activate'),
    #OAuth Social Login URL
    path('oauth/', include('social_django.urls', namespace='social')),
    #User Profile
    path('profile/<username>', UserProfile.user_profile, name='user_profile'),
    #Edit Profile
    path('editprofile/<username>', EditUserProfile.edit_user_profile, name='edit_user_profile'),
    #Delete user
    path('deleteprofile/<username>', DeleteProfile.delete, name='delete_profile'),



]

from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import GetUserView, LogoutView, SigninView, SignupView


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('signup/',include('rest_auth.registration.urls')),
    path('sign-up/', SignupView.as_view(), name="signUp"),
    path('sign-in/', SigninView.as_view(), name="signIn")
]

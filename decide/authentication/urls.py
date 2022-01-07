from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from authentication.views import *


urlpatterns = [

    path('registrarse/', inicio_registro),
    path('cerrar_sesion/', cerrar_sesion),
    path('iniciar_sesion/', iniciar_sesion),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('activate/<id>/<token>/', activate, name='activate'), 
]

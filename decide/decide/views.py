from django.shortcuts import render

# Clase que renderizara el home
class Home:
    def home(request):

        context = {}
        context['profileUrl'] = "/authentication/profile/" + request.user.username
        #Si el usuario está autenticado, cargamos un home adecuado para ello
        if request.user.is_authenticated:
            return render(request, 'home_auth.html', context)
        #Si no lo está, se carga el home por defecto con los botones de Login y Registro
        else:
            return render(request, 'home.html')
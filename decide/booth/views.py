import json
import datetime

from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CrearUsuario
from voting.views import VotingView, VotingUpdate
from voting.models import Voting, Question, PoliticalParty

# Create your views here.


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'
    '''q = Question.objects.create(desc="¿Esto es un ejemplo?")
    p = PoliticalParty.objects.create(name="Political23313", acronym="P223133", description="Esto es una descripción", leader="Líder2", president="Presidente2")
    v = Voting.objects.create(name="Votación 1", desc="Esto es un ejemplo", question=q, political_party=p, start_date="2021-01-12 00:00", end_date="2021-01-30 00:00", url="http://localhost:8000/booth/")'''

    def get_context_data(self, **kwargs):
        
        x = {
            "voting_id": 4,
            "name": "Votacion 1",
            "desc": "Esto es un ejemplo",
            "question": {
                "desc": "¿Esto es un ejemplo?"},
            "political_party": {
                "name":"Fiesta politica",
                "acronym": "FP",
                "description": "Esto es una fiesta politica",
                "leader": "Líder de la fiesta",
                "predident": "Presidente de la fiesta"},
            "start-date":"2021-01-12 00:00",
            "end-date":"2021-01-30 00:00",
            "url":"http://localhost:8000/booth/4",
            "pub-key": "a1s2d3f4g5h6j7k8l9"
            }
        
        '''context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)
        print(vid)
        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)
                print(str(v))

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS'''
        x['KEYBITS'] = settings.KEYBITS
        print(x)
        y = json.dumps(x)
        print(y)
        return y

    
def prueba(request):
    if request.method == 'GET':
        request = VotingView.get(self, request)
    if request.method == 'POST':
        request = VotingView.post(self, request)
    return render(request, "booth/booth.html")


def loginPage(request):
	    if request.user.is_authenticated:
		    return redirect('welcome')
	    else:
		    if request.method == 'POST':
			    username = request.POST.get('username')
			    password = request.POST.get('password')

			    user = authenticate(request, username=username, password=password)

			    if user is not None:
				    login(request, user)
				    return redirect('welcome')
			    else:
				    messages.info(request, 'Usuario o contraseña incorrectos')

		    context = {}
		    return render(request, 'booth/login.html', context)


def welcome(request):
    return render(request, "booth/welcome.html")


def logoutUser(request):
	logout(request)
	return redirect('login')


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('welcome')
	else:
		form = CrearUsuario()
		if request.method == 'POST':
			form = CrearUsuario(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')

				return redirect('login')

		context = {'form':form}
		return render(request, 'booth/register.html', context)

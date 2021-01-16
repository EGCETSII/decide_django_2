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
from rest_framework.renderers import TemplateHTMLRenderer
from lib2to3.fixes.fix_input import context
# Create your views here.


# TODO: check permissions and census
class BoothView(TemplateView):
    renderer_classes = [TemplateHTMLRenderer]
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
                "yesorno": "¿Esto es un ejemplo?",
                "options": {
                    "y": "Yes",
                    "n": "No"}},
            "start_date":"2021-01-08T15:29:52.040435",
            "end_date":None,
            "url":"http://localhost:8000/booth/4",
            "pub-key": "a1s2d3f4g5h6j7k8l9",
            "voted": False
            }
        
        y = {
            "voting_id": 4,
            "name": "Votacion 1",
            "desc": "Esto es un ejemplo",
            "question": {
                "multiple": "¿Esto es un ejemplo?",
                "options": {
                    "1": "Yes",
                    "2": "No",
                    "3": "NS/C"}},
            "start_date":"2021-01-08T15:29:52.040435",
            "end_date":"2021-01-20T15:29:52.040435",
            "url":"http://localhost:8000/booth/4",
            "pub-key": "a1s2d3f4g5h6j7k8l9",
            "voted": False
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
        
        y['start_date'] = self.format_fecha(y['start_date'])
        y['end_date'] = self.format_fecha(y['end_date'])
        y['KEYBITS'] = settings.KEYBITS
        y['voting'] = json.dumps(y)
        
        return y
    
    # formateo fecha "2021-01-12 00:00",
        
    def format_fecha(self, fecha):
        result = None
        
        if fecha != None:
            fecha = fecha.replace("T", " ").replace("Z", "")
            date_time = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S.%f')
            result = date_time.strftime('%d/%m/%Y a las %H:%M:%S')

        return result

    
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

from django.shortcuts import render, redirect
from decide import settings

from django.views.generic import TemplateView

from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from django.contrib.sites.shortcuts import get_current_site  
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist, ViewDoesNotExist

from .serializers import UserSerializer
from django.contrib.auth.forms import AuthenticationForm
from authentication.forms import SignUpForm
from django.contrib.auth import login, authenticate, logout
from authentication.forms import *
from django.http import HttpResponse
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage  
from .tokens import account_activation_token  
import base64

from voting.models import Voting
from census.models import Census



#Validación formulario y envío de email
def inicio_registro(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            current_site = get_current_site(request)  
            mail_subject = 'Código de verificación del registro en DECIDE'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':str(user.pk),
                'token':account_activation_token.make_token(user),  
            })  
            
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            mensaje="Por favor, compruebe su correo electrónico y confirme el enlace para completar el registro."
            return render(request, 'check_email.html', {'mensaje':mensaje,'STATIC_URL':settings.STATIC_URL})  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'STATIC_URL':settings.STATIC_URL})    


#Validación email
def activate(request,id, token):   
    try:     
        user = User.objects.get(pk=int(id))  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
         user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Gracias por confirmar su cuenta. Ya puede iniciar sesión. Cierre esta pestaña.')  
    else:  
        return HttpResponse('Este enlace de confirmación no es válido.')          


def inicio(request):
    return render(request, 'inicio.html', {'STATIC_URL':settings.STATIC_URL})

def cerrar_sesion(request):
    logout(request)
    return render(request, 'inicio.html', {'STATIC_URL':settings.STATIC_URL})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request, username=username,password=password)
            
            if user is not None:
                login(request, user)
                
                return redirect(inicio)
    
    else:
        form=AuthenticationForm()
    return render(request, 'signin.html', {'form': form, 'STATIC_URL':settings.STATIC_URL})    


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            is_superuser = request.data.get('is_superuser', False)
            if is_superuser:
                print('AAAAA')
                user = User(username=username , is_superuser=is_superuser)
            else:
                user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)
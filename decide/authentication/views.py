from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer

from django.shortcuts import render, redirect
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import RegisterForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
 
from .tokens import account_activation_token
 
from .models import Profile
from .forms import UpdateProfile


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
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)


#Sign Up View
class RegisterGUI:
    def register(request):
        if request.user.is_authenticated:
            return redirect('/')
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                #Setting the additional fields on the BBDD
                user = form.save()
                user.refresh_from_db()
                user.profile.email = form.cleaned_data.get('email')
                user.profile.first_name = form.cleaned_data.get('first_name')
                user.profile.last_name = form.cleaned_data.get('last_name')
                user.is_active = False
                user.save()
                #Email verification handler
                current_site = get_current_site(request)
                subject = 'Your Decide account needs activation'
                message = render_to_string('account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)

                return redirect('account_activation_sent')
            else:
                return render(request, 'register.html', {'form': form})
        else:
            form = RegisterForm()
            return render(request, 'register.html', {'form': form})

#Simple logout, could be improved

class LogOutTestView:
    def logout(request):
        logout(request)
        return redirect('/')

#Activation View
class AccountActivation:
    #Activation method
    def activate(request, uidb64, token):
        try:
            #Extracting the token
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        #Token verification and account activation
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend = 'base.backends.AuthBackend')
            return HttpResponse('Thank you for verifying your email, you can login your account now')
        else:
            return render(request, 'account_activation_invalid.html')
 
    #Account activation sent view
    def account_activation_sent(request):
        return render(request, 'account_activation_sent.html')

#User Profile
class UserProfile:
    def user_profile(request, username):
        user = User.objects.get(username=username)
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        context = {
            "user": user
        }
        selfusername = request.user.username
        if not username == selfusername:
            return HttpResponse('You are not authorized to see this page.')

        return render(request, 'user_profile.html', context={'username': username,'first_name': first_name, 'last_name': last_name, 'email': email})

class ProfileView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)
        
        username = user.profile.username
        if not username:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        return Response(request, 'user_profile.html', context)

#User Profile
class EditUserProfile:
    def edit_user_profile(request, username):
        user = User.objects.get(username=username)
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        context = {
            "user": user
        }
        selfusername = request.user.username
        if not username == selfusername:
            return HttpResponse('You are not authorized to see this page.')
        if request.method == 'POST':
         form = UpdateProfile(request.POST, instance=request.user)
         form.actual_user = request.user
         if form.is_valid():
                form.save()
                username = form.actual_user.username
                first_name = form.actual_user.first_name
                last_name = form.actual_user.last_name
                email = form.actual_user.email
                return render(request, 'user_profile.html', context={'username': username,'first_name': first_name, 'last_name': last_name, 'email': email}) 
         elif request.POST.get('username') == '':         
             messages.error(request, 'El nombre de usuario de puede estar vacío.')
         elif User.objects.get(username=request.POST.get('username')).DoesNotExist:
             messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            form = UpdateProfile()
        return render(request, 'edit_user_profile.html', context={'username': username,'first_name': first_name, 'last_name': last_name, 'email': email})

class EditProfileView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = user.profile.username
        if not username:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        return Response(request, 'user_profile.html', context)

#Creamos los controladores para el borrado de usuario y su conveniente redireción 
class DeleteProfile:
    def delete(request, username):
        user = User.objects.get(username=username)
        username = user.username
        selfusername = request.user.username
        if not username == selfusername:
            return HttpResponse('You are not authorized to see this page.')
        if request.method == 'POST':
            form = UpdateProfile(request.POST, instance=request.user)
            form.actual_user = request.user
            if request.POST.get('deleteprofile') == 'BORRAR':
                try:
                    user = User.objects.get(username=username)
                    user.delete()
                    return redirect('../../')
                except User.DoesNotExist:
                    messages.error(request, "El usuario no existe")
            elif request.POST.get('deleteprofile') != 'BORRAR':         
                messages.error(request, 'Por favor, escriba la parabra solicitada.')
        return render(request, 'delete_profile.html')

class DeleteProfileView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = user.profile.username
        if not username:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        return Response(request, 'logingui.html')

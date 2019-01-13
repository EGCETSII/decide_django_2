from rest_framework import serializers
from allauth.utils import (email_address_exists,
                               get_username_max_length)
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_settings
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from allauth.account.utils import setup_user_email

from .models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')


class UserSignupSerializer(RegisterSerializer):

    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    gender = serializers.CharField(max_length=10)
    birthdate = serializers.DateTimeField()

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'gender': self.validated_data.get('gender',''),
            'birthdate': self.validated_data.get('birthdate', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)

        #Assign gender and birthdate to the new user
        userProfile = UserProfile(user=user,gender=self.validated_data.get('gender',''),birthdate=self.validated_data.get('birthdate',''))
        userProfile.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
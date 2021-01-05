from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
from .ldapMethods import LdapCensus
#from authentication.models import User
from django.contrib.auth.models import User
from voting.models import Voting
from django.db import models
from census.forms import CensusAddLdapForm
from django.shortcuts import render, redirect
from django.contrib import messages

#Metodos propios


#Formulario

def importCensusFromLdap(request):
        
        if request.user.is_staff:

            if request.method == 'POST':
                form = CensusAddLdapForm(request.POST)

                if form.is_valid():
                    urlLdap = form.cleaned_data['urlLdap']
                    treeSufix = form.cleaned_data['treeSufix']
                    pwd = form.cleaned_data['pwd']
                    branch = form.cleaned_data['branch']
                    #group = form.cleaned_data['group']
                    voting = form.cleaned_data['voting'].__getattribute__('pk')

                    voters = User.objects.all()
                    usernameList = LdapCensus().LdapGroups(urlLdap, treeSufix, pwd, branch)
                    
                    userList = []
                    for username in usernameList:
                        
                        user = voters.filter(username=username)
                        if user:
                            user = user.values('id')[0]['id']
                            userList.append(user)
                        
                if request.user.is_authenticated:
                    #voters_ids = userList.values_list('id', flat=True, named=False)
                        
                    for username in userList:
                        #if not is_exist_
                        
                        census = Census(voting_id=voting, voter_id=username)
                        census.save()

                return redirect('/admin/census/census')
            else:
                form = CensusAddLdapForm()

            context = {
                'form': form,
            }
            return render(request, template_name='importCensusLdap.html', context=context)
        else:
            messages.add_message(request, messages.ERROR, "permiso denegado")
            return redirect('/admin')
                    
def main_census(request):

    census = Census.objects.all()
    votings = Voting.objects.all()
    voters = User.objects.all()
    return render(request,"main_index.html",{'census': census, 'votings':votings, 'voters':voters})
        



#Metodos iniciales
class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)
    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})

class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')
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
from django.contrib.auth.models import User

from django.db import models




class CensusCreate(generics.ListCreateAPIView):
    #permission_classes = (UserIsStaff,)
    """
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
    """
    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})

    def create(self, request, *args, **kwargs):
        urlLdap = request.data.get('urlLdap')
        userDomain = request.data.get('treeSufix')
        psw = request.data.get('psw')
        group = request.data.get('group')
        voting_id = request.data.get('voting_id')
        try:
            usernameList = LdapCensus().sacaMiembros(urlLdap, userDomain, psw, group)
            for userName in usernameList:
                user = User.objects.get(username=userName)
                if user:
                    census = Census(voting_id=voting_id, voter_id=user.pk)
                    census.save()
                #else:
                    #TODO
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)


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


"""
class CensusLdap(generics.RetrieveDestroyAPIView):
   

    def retrieve(self, request, *args, **kwargs):
        ldapUrl = request.GET.get('urlLdap')
        dominio = request.GET.get('dominio')
        psw = request.GET.get('psw')
        grupo = request.GET.get('grupo')
        CensusLdapObject.objects.get
        censo = CensusLdap().sacaMiembros(ldapUrl, dominio, psw, grupo)
        return Response({'censo': censo})

"""
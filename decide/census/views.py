import django_filters.rest_framework
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
from .serializers import CensusSerializer


class CensusCreate(generics.ListCreateAPIView):
    queryset = Census.objects.all()
    serializer_class = CensusSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voting_id',)

    def post(self, request, *args, **kwargs):
        """Creation of census
        ---
        # Body parameters:
        - **voting_id**: ID of the voting you want to add a census into
        - **voters**: List of voters_ids that you want to add to the votation
        # Example request
        '''
        {
            "voting_id": 1,
            "voters": [
                1, 2, 3
            ]
        }
        '''
        """
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=int(voter))
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def get(self, request, *args,**kwargs):
        """List of voters from votation
        ---
        ### Entering a voting_id will return the census associated with it:
        ## Description field by field:
        - **voting_id**: ID of the voting
        """
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):
    queryset = Census.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voter_id',)

    def destroy(self, request, voting_id, *args, **kwargs):
        """Delete a census
         ---
         ### Delete an specific census:
         ## Description field by field:
         - **voting_id** ***mandatory***: ID of the voting
         - **voter_id**: ID of the voter
         """
        voter_id = request.GET.get('voter_id')
        census = Census.objects.filter(voting_id=voting_id, voter_id=voter_id)
        if len(census) == 0:
            return Response('Invalid voter', status=ST_401)
        census.delete()
        return Response('Voter deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        """Check a single voter from voting
         ---
         ### You can check if an especific voter is registered in a voting:
         ## Description field by field:
         - **voting_id** ***mandatory***: ID of the voting
         - **voter_id**: ID of the voter
         """
        voter_id = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter_id)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

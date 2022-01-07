from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics

from .models import Vote
from .serializers import VoteSerializer
from base import mods
from base.perms import UserIsStaff


class StoreView(generics.ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('voting_id', 'voter_id')

    def get(self, request):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        return super().get(request)

    def post(self, request):
        """
         * voting: id
         * voter: id
         * votes: [ { "a": int, "b": int } , { "a": int, "b": int } ]
        """

        vid = request.data.get('voting')
        voting = mods.get('voting', params={'id': vid})
        if not voting or not isinstance(voting, list):
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting[0].get('start_date', None)
        end_date = voting[0].get('end_date', None)
        not_started = not start_date or timezone.now() < parse_datetime(start_date)
        is_closed = end_date and parse_datetime(end_date) < timezone.now()
        if not_started or is_closed:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter')
        votes = request.data.get('votes')
        

        if not vid or not uid or not votes:
            
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        try:
            token = request.auth.key
        except:
            token= request.data.get("token")
        
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        
        # borrar   self.assertEqual(response.status_code, 403)
        usuario_ha_votado= True if (Vote.objects.filter(voter_id=voter_id,voting_id=vid).count()!=0) else False
    
        
        if not voter_id or voter_id != uid or usuario_ha_votado:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        for vote in votes:
           
            a = vote.get("a")
            b = vote.get("b")

            
            v= Vote.objects.create(voting_id=vid, voter_id=uid, a=a, b=b)
            v.save()
            

        return  Response({})

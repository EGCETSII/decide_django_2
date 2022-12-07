from Crypto.PublicKey import ElGamal
from django.utils import timezone
from django.utils.dateparse import parse_datetime
import django_filters.rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import get_object_or_404

from voting.models import Voting
from .models import Vote
from .serializers import VoteSerializer
from base import mods
from base.perms import UserIsStaff

from decide import settings
from mixnet.mixcrypt import MixCrypt


def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
    pk = v.pub_key
    p, g, y = (pk.p, pk.g, pk.y)
    k = MixCrypt(bits=bits)
    k.k = ElGamal.construct((p, g, y))
    return k.encrypt(msg)

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
        Store a vote
        ---
        ### Keep in mind that storing a vote will take some time to be executed.
        # Pre-requisites
        - You need to be logged in, and have your token in the request
        - You need to be registered in the census of the voting
        - The voting must be started, and not stopped
        ---
        # Body Parameters
         - **voting_id**: id -- Voting id
         - **voter_id**: id -- Voter id
         - **opt_number**: int -- Number of the option chosen
         - **token**: string -- Auth token of the user who is casting the vote, must be the same user as voter_id
        """

        vid = request.data.get('voting_id')
        voting = get_object_or_404(Voting, pk=vid)
        if not voting:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        start_date = voting.start_date
        end_date = voting.end_date
        not_started = not start_date or timezone.now() < start_date
        is_closed = end_date and end_date < timezone.now()
        if not_started or is_closed:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        uid = request.data.get('voter_id')
        #vote = request.data.get('vote')

        if not vid or not uid:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # validating voter
        token = request.data.get('token')
        voter = mods.post('authentication', entry_point='/getuser/', json={'token': token})
        voter_id = voter.get('id', None)
        if not voter_id or voter_id != uid:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        # the user is in the census
        perms = mods.get('census/{}'.format(vid), params={'voter_id': uid}, response=True)
        if perms.status_code == 401:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

        a, b = encrypt_msg(self, request.data.get('opt_number'), voting)

        defs = { "a": a, "b": b }
        v, _ = Vote.objects.get_or_create(voting_id=vid, voter_id=uid,
                                          defaults=defs)
        v.a = a
        v.b = b

        v.save()

        return  Response({})

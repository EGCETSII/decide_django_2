import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from census.models import ParentGroup
from rest_framework.status import (
        HTTP_409_CONFLICT as ST_409
)
from django.db.utils import IntegrityError


from .models import ChildVoting, Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from census.models import Census
import re


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id', )

    def get(self, request, *args, **kwargs):
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # Coges el id de cada grupo de la votación
        groups = request.data.get('groups')

        # Comprueba que el id del grupo no es null o blank
        if (groups != '' and groups!=None):
            if not (re.match('^[\d,]+$', groups)):
                return Response({}, status=status.HTTP_400_BAD_REQUEST)


            # Comprueba si alguno de los grupos no existe
            ids = list(groups.split(","))
            for id in ids:
                try:
                    ParentGroup.objects.get(pk=int(id))
                except:
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)

        #Creación de la pregunta
        question_type= request.data.get('question_type')

        if (question_type!='' and question_type!=None and question_type!= 'SO' and  question_type!='MC'):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
            
        question = Question(desc=request.data.get('question'),type= question_type if (question_type!='' and question_type!=None) else 'SO' )
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                question=question)
        voting.save()
        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)


	    ################
        # Añadir todos los usuarios del grupo a la votación

        
        voting_id = voting.pk
        if (groups != '' and groups!=None):

            # Obtener todos los usuarios que pertenecen al grupo
            for id in ids:
                group = ParentGroup.objects.get(pk=int(id))
                voters = User.objects.filter(groups=group)
                ChildVoting.objects.create(parent_voting=Voting.objects.get(pk=voting_id),group=group)

                # Por cada usuario
                # Añadir al censo de dicha votación
                try:
                    for voter in voters:
                        census, isCreated = Census.objects.get_or_create(voting_id=voting_id, voter_id=voter.pk)  
                        if isCreated:
                            census.save()  
                except IntegrityError:
                    return Response('Error try to create census', status=ST_409)
                
            ###############
        else:
            group = ParentGroup.objects.create(name='Users with no group ' + str(voting_id), isPublic=True)
            ChildVoting.objects.create(parent_voting=Voting.objects.get(pk=voting_id),group=group)



        return Response(data={'id': voting_id}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.create_pubkey()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = 'Voting stopped'
        elif action == 'tally':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = 'Voting is not stopped'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = 'Voting already tallied'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)
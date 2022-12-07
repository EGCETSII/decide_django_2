import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer, VotingActionSerializer
from base.perms import UserIsStaff
from base.models import Auth
from rest_framework.views import APIView


class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = SimpleVotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('id',)
    lookup_field = ('question-detail',)


    def get(self, request, *args, **kwargs):
        """Lists or show votings
        ---
        ### You can either:
        - *Show a single voting*: Entering its id
        - *List all votings*: Not giving any parameter in the request
        ## Description field by field:
        - **id**: ID of the voting
        """
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v1':
            self.serializer_class = VotingSerializer
        res = super().get(request, *args, **kwargs)
        return res

    def post(self, request, *args, **kwargs):
        """
        Create a Voting with a new question
        ---
        ### In order to create a voting, you will need to generate an authentication token by logging in. Then, add it to the parameter "token"
        # Body Parameters
        - **name**: Title of the voting
        - **desc**: Description of the voting
        - **question**: Describe the question to be asked in the voting
        - **question_opt**: A list containing each of the available options for the voting. Ex: ['cat','dog','horse]
        - **token**: Auth token of an user with voting permissions
        # Example request
        ```
        {
            "name": "Voting 1",
            "desc": "Voting 1 description",
            "question": "What is your favorite animal?",
            "question_opt": {"cat":1,"dog":2,"horse":3},
            "token": 21398suhdud9182u8381uediqh9128
        }
        ```
        """
        request.auth = request
        request_data = request.data
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request_data:
                return Response(f"Cant find parameter {data} in your request", status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request_data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request_data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request_data.get('name'), desc=request_data.get('desc'),
                question=question)
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.UpdateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingActionSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    #permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        """
        Start/Stop/Tally a voting
        ---
        ### Keep in mind that some actions will take some time to be executed. For example, if you start a voting, it will take some time to generate its pub_keys.
        # Pre-conditions
        - The voting must exist
        - The correct order of actions is Start -> Stop -> Tally
        - Votes can be casted only when the voting is started, a closed voting wont accept votes
        - You need to provide the correct token
        ---
        # Parameters
        - **id**: ID of the voting
        # Body Parameters
        - **action**: start, stop, tally. In that order, they will start the voting, stop it and tally the results
        - **token**: Auth token of an user with voting management permissions
        """
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
                voting.tally_votes(token=request.data.get('token'))
                msg = 'Voting tallied'
        else:
            msg = 'Action not found, try with start, stop or tally'
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)

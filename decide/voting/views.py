import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from dotenv import load_dotenv
import os

load_dotenv("voting/.env")
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

        question = Question(desc=request.data.get('question'))
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
        return Response({}, status=status.HTTP_201_CREATED)

class BotMessageHandler():
    def create_bot_message_start(r):
        # Creamos el String de la v1 del módulo
        # TODO: URL del front
        URL = os.getenv("URL")
        mensaje = "Se acaba de comenzar una votación, entra en " + URL + r + " para poder acceder a ella."
        return mensaje


    def create_bot_message_tally(r):
        # Vamos a obtener las propiedades del resultado de la votación
        voting_id = "ID de la votación: " + str(r[0]['id']) + "\n"
        voting_name = "Nombre de la votación: " + str(r[0]['name']) + "\n"
        voting_desc =  "Descripción de la votación: " + str(r[0]['desc']) + "\n"
        voting_question = "Cuestión que se debate en la votación: " + str(r[0]['question']['desc']) + "\n"

        # Aquí vamos a crear la lista de opciones para el mensaje
        voting_options = r[0]['question']['options']
        voting_options_to_message = "Opciones de la encuesta: \n"

        for option in voting_options:
            voting_options_to_message += "Opción " + str(option['number']) + " -> " + str(option['option']) + "\n"

        voting_start_date_without_format = str(r[0]['start_date']).split(sep='.')[0].split(sep='T')[0]
        voting_end_date_without_format = str(r[0]['end_date']).split(sep='.')[0].split(sep='T')[0]

        #Formateamos la fecha de inicio de la votación
        date_start_splitted = voting_start_date_without_format.split(sep='-')
        day_start = date_start_splitted[2]
        month_start = date_start_splitted[1]
        year_start = date_start_splitted[0]
        voting_start_date_formatted = "Votación creada el " + day_start + "/" + month_start + "/" + year_start
        voting_start_date_time = " a las " + str(r[0]['start_date']).split(sep='.')[0].split(sep='T')[1] + "\n"

        #Formateamos la fecha de fin de la votación
        date_end_splitted = voting_end_date_without_format.split(sep='-')
        day_end = date_end_splitted[2]
        month_end = date_end_splitted[1]
        year_end = date_end_splitted[0]
        voting_end_date_formatted = day_end + "/" + month_end + "/" + year_end
        voting_end_date_time = str(r[0]['end_date']).split(sep='.')[0].split(sep='T')[1]

        voting_tally = str(r[0]['tally'][0])
        voting_postproc = r[0]['postproc']

        voting_options_postproc_to_message = ""

        for result in voting_postproc:
            voting_options_postproc_to_message += "Opción " + str(result['number']) + " -> " + str(result['option']) + " ---> " + str(result['votes']) + " votos." + "\n"
        message_tally1 = "\n\nDespués de haber realizado el recuento de votos el " + voting_end_date_formatted + " a las " + voting_end_date_time
        message_tally2 = message_tally1 + " se han obtenido los siguientes resultados: \nHan votado: " + voting_tally + " personas, distribuidas en las siguientes opciones: \n\n"
        # Creamos el String de la v1 del módulo
        mensaje_botPart1 = voting_id + voting_name + voting_start_date_formatted + voting_start_date_time + voting_desc
        mensaje_bot = mensaje_botPart1 + voting_question + voting_options_to_message + message_tally1 + message_tally2 + voting_options_postproc_to_message

        return mensaje_bot


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

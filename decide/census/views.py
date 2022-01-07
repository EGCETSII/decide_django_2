import logging as log
import json
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User,Group
from django.http.response import HttpResponse
from django.shortcuts import render

from django.db.utils import IntegrityError
from django.views.generic import TemplateView
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import View
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import ParentGroupSerializer
from rest_framework.status import (
    HTTP_201_CREATED as ST_201,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_401_UNAUTHORIZED as ST_401,
    HTTP_409_CONFLICT as ST_409
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from base.perms import UserIsStaff
from .models import Census, ParentGroup, Request
from decide import settings
from .forms import GroupOperationsForm

group_successfully_created = "Grupo creado con éxito"
operations_template = 'group_operations.html'

from django.views.generic.base import View
from census.import_and_export import *
from census.forms import *
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from decide import settings


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
        voters = Census.objects.filter(
            voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(
            voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')


class GroupOperationsAPI(generics.CreateAPIView):
    permissions_classes = (permissions.IsAuthenticated,)

    def check(self, user, group_name, base_group, groups, is_public):
        if not group_name or not isinstance(group_name, str) or group_name.isspace():
            return Response('Group name is required', status=ST_400)

        group_name = group_name.strip()
        if ParentGroup.objects.filter(name=group_name).exists():
            return Response(f'Group with name \'{group_name}\' already exists, please, try another name', status=ST_409)

        if not base_group or not isinstance(base_group, str):
            return Response('Base group: str is required', status=ST_400)

        if not groups or not isinstance(groups, list) or any(not isinstance(group, str) for group in groups) or len(groups) < 1:
            return Response('groups: list[str] must have one group: str at least', status=ST_400)

        if not isinstance(is_public, bool):
            return Response('If you wish the group to be private you must set \'is_public\' attribute to false, otherwise set it to true', status=ST_400)

        try:
            if user not in ParentGroup.objects.get(name=base_group).voters.all():
                return Response('User must be in all groups to perform this action', status=ST_401)
        except ObjectDoesNotExist:
            return Response(f'There is no group with name \'{base_group}\', please, try again', status=ST_400)

        for group in groups:
            try:
                if user not in ParentGroup.objects.get(name=group).voters.all():
                    return Response('User must be in all groups to perform this action', status=ST_401)
            except ObjectDoesNotExist:
                return Response(f'There is no group with name \'{group}\', please, try again', status=ST_400)

        if base_group in groups:
            return Response('Base group must not be in groups', status=ST_400)

        return None

    def create(self, request, *args, **kwargs):
        group_name = request.data.get('name')
        base_group = request.data.get('base_group')
        groups = request.data.get('groups')
        is_public = request.data.get('is_public')
        user = request.user

        response = self.check(
            user=user, group_name=group_name, base_group=base_group, groups=groups, is_public=is_public)
        if response:
            return response

        base_group = ParentGroup.objects.get(name=base_group)
        groups = [ParentGroup.objects.get(name=group) for group in groups]

        url = request.path.split('/census/')[1]

        GroupOperations().operate(
            group_name=group_name, base_group=base_group, groups=groups, is_public=is_public, operation=url)

        return Response(group_successfully_created, status=ST_201)


class GroupOperations(View):

    @method_decorator(login_required(login_url='/authentication/iniciar_sesion'))
    def get(self, request, *args, **kwargs):
        form = GroupOperationsForm()
        form.fields['base_group'].queryset = request.user.parentgroup_set.all()
        form.fields['groups'].queryset = request.user.parentgroup_set.all()
        context = {'form': form, 'STATIC_URL': settings.STATIC_URL}
        return render(request, operations_template, context=context)

    @ method_decorator(login_required(login_url='/authentication/iniciar_sesion'))
    def post(self, request, *args, **kwargs):
        form = GroupOperationsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.operate(
                cd['group_name'],
                cd['base_group'],
                cd['groups'],
                cd['is_public'],
                cd['operation'])
            context = {'form': form, 'STATIC_URL': settings.STATIC_URL,
                       'message': group_successfully_created}
            return render(request, operations_template, context=context)
        else:
            form.fields['base_group'].queryset = request.user.parentgroup_set.all()
            form.fields['groups'].queryset = request.user.parentgroup_set.all()
            context = {'form': form, 'STATIC_URL': settings.STATIC_URL}
            return render(request, operations_template, context=context)

    def operate(self, group_name, base_group, groups, is_public, operation):
        new_group: ParentGroup = ParentGroup.objects.create(
            name=group_name, isPublic=is_public)
        qs = User.objects.none()
        if operation == 'union':
            qs = self.union(base_group, groups)
        elif operation == 'intersection':
            qs = self.intersection(base_group, groups)
        elif operation == 'difference':
            qs = self.difference(base_group, groups)
        new_group.voters.set(qs)

    def union(self, base_group, groups):
        qs = base_group.voters.all()
        for group in groups:
            qs = qs.union(group.voters.all())
        return qs

    def intersection(self, base_group, groups):
        qs = base_group.voters.all()
        for group in groups:
            qs = qs.intersection(group.voters.all())
        return qs

    def difference(self, base_group, groups):
        qs = base_group.voters.all()
        for group in groups:
            qs = qs.difference(group.voters.all())
        return qs


class ImportExportGroup(View):
    ### Importar/Exportar


    FILE_PATH = 'authentication/files/'
    FORMATS = {'excel':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'txt': 'text/plain'}


    @csrf_exempt
    @login_required(login_url='/authentication/iniciar_sesion')
    def importGroup(request):
        form = importForm()

        if not request.user.is_superuser:
            return render(request, 'inicio.html', {'STATIC_URL':settings.STATIC_URL})

        if request.method == 'POST':
            form = importForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data['name'] 
                is_public = form.cleaned_data['is_public']
                file = request.FILES['file']
                format = file.content_type

                users_list = []
                # Si file es excel, guardo el archivo para abrirlo después
                if (format == ImportExportGroup.FORMATS['excel']):
                    path = default_storage.save(ImportExportGroup.FILE_PATH + 'temp_import.xlsx', ContentFile(file.read()))
                    users_list = readExcelFile(path)
                    os.remove(os.path.join(path))   # Borro el archivo tras su uso
                # Si file es txt, no necesito guardar el fichero
                elif (format == ImportExportGroup.FORMATS['txt']):
                    users_list = readTxtFile(file)
                else:
                    messages.error(request, "Formato de archivo no válido.")
                    return render(request, 'import_group.html', {'form': form, 'STATIC_URL':settings.STATIC_URL})

                # Si todos los usuarios existen, creo el grupo y añado todos los usuarios de la lista
                if (users_list != None):
                    b = createGroup(name, users_list, is_public)
                    # Si b==False, entonces ya existía un grupo con mismo nombre
                    if (b):
                        messages.success(request, "Grupo creado correctamente.")
                    else:
                        messages.success(request, "Grupo actualizado correctamente.")
                else:
                    messages.error(request, "Uno de los usuarios indicados no existe.")

        return render(request, 'import_group.html', {'form': form, 'STATIC_URL':settings.STATIC_URL})
            

    @csrf_exempt
    @login_required(login_url='/authentication/iniciar_sesion')
    def exportGroup(request):
        form = exportForm()

        if not request.user.is_superuser:
            return render(request, 'inicio.html', {'STATIC_URL':settings.STATIC_URL})

        if request.method == 'POST':
            form = exportForm(request.POST, request.FILES)
            if form.is_valid():
                group = form.cleaned_data['group']
                users = User.objects.filter(groups=group)
                
                # Crea el Excel con los usuarios exportados
                writeInExcelUsernames(users, ImportExportGroup.FILE_PATH + 'temp_export.xlsx', 'temp_export.xlsx')
                    
                # Abrir el Excel generado
                with open(ImportExportGroup.FILE_PATH + 'temp_export.xlsx', 'rb') as excel:
                    data = excel.read()

                # Automáticamente descarga el archivo
                resp = HttpResponse(data, content_type=ImportExportGroup.FORMATS['excel'])
                resp['Content-Disposition'] = 'attachment; filename=export_group.xlsx'
                return resp

        return render(request, 'export_group.html', {'form': form, 'STATIC_URL':settings.STATIC_URL})


# Listado de grupos públicos y privados
class joinGroup(APIView):
    
    def post(self, request):
            #Obtener grupo y usuario
            id_group= int(request.data.get('group_to_join'))        
            id_user= int(request.data.get('userId'))

            try:
                group = ParentGroup.objects.get(pk=id_group)
                user = User.objects.get(pk=id_user)
                voters = group.voters.all()
                userIsInTheGroup= user in voters

                print(group.voters)
                # Añadir usuario al grupo 
                if group!=None and user!= None and not userIsInTheGroup: #Comprobar también que el usuario no está ya en el grupo....
                    
                    if group.isPublic:
                        
                        group.voters.add(user)
                        
                        return Response({})

                    elif group.isPublic == False:
                        request = Request(voter_id=id_user, group_id=id_group)
                        request.save()
                        return Response({})

                #Grupo en el que ya está el usuario
                else:
                    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            except:
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)

# TODO: check permissions and census
class GroupsView(TemplateView):
    template_name = 'groupList.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = ParentGroup.objects.all()

        diccionario= {}
        for group in groups:
            diccionario[group.pk]= {"name": group.name, "isPublic": group.isPublic }
       
        
        context['groups_info'] = diccionario
        context['KEYBITS'] = settings.KEYBITS

        return context
 
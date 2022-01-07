from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting
from django.core.mail import send_mail

from .filters import StartedFilter

from django.contrib.auth.models import User, Group
from census.models import Census



def start(modeladmin, request, queryset):
    
    
    for v in queryset.all():
    # #IDs de los usuarios que puede participar en la votación
        users_id=list(Census.objects.filter(voting_id=v.id).values_list('voter_id', flat=True))
        users_email = []
        for u in users_id:
            users_email.extend(list(User.objects.filter(id=u).values_list('email',flat = True)))
        send_mail('Nueva votación creada', 'Ha comenzado una nueva votación en la que puedes participar',
        'decidepartchullo@gmail.com', users_email, fail_silently=False)  
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
   
    for v in queryset.filter(end_date__lt=timezone.now()):
        
        token = request.session.get('auth-token', '')
        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'deadline')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Borro todos los censos de la votacion (actualizar la votacion)
        voting_id = Voting.objects.get(pk=obj.pk).pk
        Census.objects.filter(voting_id=voting_id).delete()

        groups = obj.groups

        # Comprueba que el id del grupo no es null o blank
        if (groups != '' and groups!=None): 
            groupsIds = list(groups.split(','))

        # Obtener todos los usuarios que pertenecen al grupo
            for id in groupsIds:
                group = Group.objects.get(pk=int(id))
                voters = User.objects.filter(groups=group)

                # Por cada usuario
                # Añadir al censo de dicha votación
                for voter in voters:
                    census, isCreated = Census.objects.get_or_create(voting_id=voting_id, voter_id=voter.pk)  
                    if isCreated:
                        census.save()           
                    


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)

from django.contrib import admin
from django.utils import timezone

from .models import QuestionOption
from .models import Question
from .models import Voting

from .filters import StartedFilter

# Votaciones normales

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 1
class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1
class VotacionAdmin(admin.ModelAdmin):
    list_display=('id','titulo','descripcion','Numero_De_Preguntas')
    inlines =[PreguntaInline]

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('id','Nombre_Votacion','textoPregunta','Numero_De_Respuestas','Media_De_Las_Respuestas','Respuesta_Maxima','Respuesta_Minima')
    inlines =[RespuestaInline]

class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('id','respuesta','Nombre_Pregunta')

def start(modeladmin, request, queryset):
    for v in queryset.all():
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
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]


admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.register(Votacion, VotacionAdmin)
admin.site.register(Pregunta,PreguntaAdmin)
admin.site.register(Respuesta,RespuestaAdmin)

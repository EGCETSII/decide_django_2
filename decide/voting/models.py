from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

from base import mods
from base.models import Auth, Key

#Votaciones binarias
# MODELO DE VOTACION BINARIA
class VotacionBinaria(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.titulo
        

#MODELO DE RESPUESTA BINARIA
class RespuestaBinaria(models.Model):
    id = models.AutoField(primary_key=True)
    votacionBinaria = models.ForeignKey(VotacionBinaria,on_delete = models.CASCADE)
    respuesta = models.BooleanField(choices =[(1,('Sí')),(0,('No'))])
    def Nombre_Votacion(self):
        return self.votacionBinaria.titulo

#Votaciones normales

#MODELO DE VOTACIONES
class Votacion(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    def __str__(self):
        return self.titulo

 #DEVUELVE EL NÚMERO DE PREGUNTAS QUE TIENE ASOCIDADA UNA VOTACION  
    def Numero_De_Preguntas(self):
        return Pregunta.objects.filter(votacion_id=self.id).count()
   #AÑADE UNA PREGUNTA  A LA VOTACION 
   #A LA HORA DE CREAR LA PREGUNTA SOLO ES NECESARIO INDICARLE EL ATRIBUTO TEXTOPREGUNTA
   # LA FUNCION SE ENCARGA DE ASOCIAR LA PREGUNTA  A LA VOTACION QUE SE LE HA INDICADO  
    def addPregunta(self,pregunta):
        pregunta.votacion = self
        pregunta.save()

#MODELO DE PREGUNTAS
class Pregunta(models.Model):
    id = models.AutoField(primary_key=True)
    votacion = models.ForeignKey(Votacion,on_delete = models.CASCADE)
    textoPregunta = models.CharField(max_length=50)
    def Nombre_Votacion(self):
        return self.votacion.titulo
    def __str__(self):
        return self.textoPregunta
        
#DEVUELVE EL NÚMERO DE VECES QUE SE HA RESPONDIDO A LA PREGUNTA
   #COINCIDE CON EL NÚMERO DE VECES QUE SE HA RESPONDIDO A LA VOTACIÓN ASOCIDADA A LA PREGUNTA
   #YA QUE EN UNA VOTACIÓN SE TIENEN QUE CONTESTAR A TODAS LAS PREGUNTAS  
    def Numero_De_Respuestas(self):
        return Respuesta.objects.filter(pregunta_id=self.id).count()

   #DEVUELVE LA CALIFICACIÓN MEDIA DE LA PREGUNTA EN BASE A LAS RESPUESTAS DADAS 
    def Media_De_Las_Respuestas(self):
        respuestas = Respuesta.objects.filter(pregunta_id=self.id).values('respuesta')
        n_respuestas = len(respuestas)
        if n_respuestas == 0:##EVITAR DIVISIÓN POR CERO 
            n_respuestas=1
        total = 0
        for value in respuestas:
            total = total + value['respuesta']
        return total/n_respuestas
    
   #DEVUELVE LA RESPUESTA MAS ALTA DADA A UNA PREGUNTA 
    def Respuesta_Maxima(self):
        max = Respuesta.objects.filter(pregunta_id=self.id).aggregate(Max('respuesta'))
        return str(max['respuesta__max'])

    #DEVUELVE LA RESPUESTA MAS BAJA DADA A UNA PREGUNTA 
    def Respuesta_Minima(self):
        min = Respuesta.objects.filter(pregunta_id=self.id).aggregate(Min('respuesta'))
        return str(min['respuesta__min'])


    #AÑADE UNA RESPUESTA  A LA PREGUNTA 
   #A LA HORA DE CREAR LA RESPUESTA SOLO ES NECESARIO INDICARLE EL ATRIBUTO RESPUESTA
   # LA FUNCION SE ENCARGA DE ASOCIAR LA RESPUESTA  A LA PREGUNTA QUE SE LE HA INDICADO
    def addRespuesta(self,respuesta):
        respuesta.pregunta = self
        respuesta.save()

#Modelo de Respuesta
class Respuesta(models.Model):
    id = models.AutoField(primary_key=True)
    pregunta = models.ForeignKey(Pregunta,on_delete = models.CASCADE)
    respuesta = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    def Nombre_Pregunta(self):
        return self.pregunta.textoPregunta

class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    option = models.TextField()

    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.option, self.number)


class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        options = self.question.options.all()

        opts = []
        for opt in options:
            if isinstance(tally, list):
                votes = tally.count(opt.number)
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = { 'type': 'IDENTITY', 'options': opts }
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name

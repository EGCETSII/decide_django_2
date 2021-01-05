from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from base import mods
from base.models import Auth, Key
from django.db.models import Max,Min


#Votaciones binarias
# MODELO DE VOTACION BINARIA
class VotacionBinaria(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.titulo


#DEVUELVE EL NÚMERO DE RESPUESTAS A TRUE QUE TIENE LA VOTACION BINARIA 
    def Numero_De_Trues(self):
        return RespuestaBinaria.objects.filter(respuesta=1,votacionBinaria_id=self.id).count()

   #DEVUELVE EL NÚMERO DE RESPUESTAS A FALSE QUE TIENE LA BOTACION BINARIA 
    def Numero_De_Falses(self):
        return RespuestaBinaria.objects.filter(respuesta=0,votacionBinaria_id=self.id).count()
   #AÑADE UNA RESPUESTA BINARIA A LA VOTACION BINARIA 
   #A LA HORA DE CREAR LA RESPUESTA BINARIA SOLO ES NECESARIO INDICARLE EL ATRIBUTO RESPUESTA
   # LA FUNCION SE ENCARGA DE ASOCIAR LA RESPUESTA BINARIA A LA VOTACION BINARIA QUE SE LE HA INDICADO  
    def addRespuestaBinaria(self,respuestaBinaria):
        respuestaBinaria.votacionBinaria = self
        respuestaBinaria.save()
        

#MODELO DE RESPUESTA BINARIA
class RespuestaBinaria(models.Model):
    id = models.AutoField(primary_key=True)
    votacionBinaria = models.ForeignKey(VotacionBinaria,on_delete = models.CASCADE,related_name="respuestasBinarias")
    respuesta = models.BooleanField(choices =[(1,('Sí')),(0,('No'))])
    def Nombre_Votacion(self):
        return self.votacionBinaria.titulo


#Votaciones normales

#MODELO DE VOTACIONES
class Votacion(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
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
    votacion = models.ForeignKey(Votacion,on_delete = models.CASCADE,related_name="preguntas")
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
    pregunta = models.ForeignKey(Pregunta,on_delete = models.CASCADE,related_name="respuestas")
    respuesta = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    def Nombre_Pregunta(self):
        return self.pregunta.textoPregunta


# VOTACIONES MÚLTIPLES
class VotacionMultiple(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.titulo
      # DEVUELVE EL NÚMERO DE PREGUNTAS QUE TIENE ASOCIDADA UNA VOTACION MULTIPLE
    def Numero_De_Preguntas_Multiple(self):
        return PreguntaMultiple.objects.filter(votacionMultiple_id=self.id).count()
#AÑADE UNA PREGUNTA MULTIPLE  A LA VOTACION MULTIPLE
    #A LA HORA DE CREAR LA PREGUNTA MULTIPLE SOLO ES NECESARIO INDICARLE EL ATRIBUTO TEXTOPREGUNTA
    #LA FUNCION SE ENCARGA DE ASOCIAR LA PREGUNTA MULTIPLE  A LA VOTACION MULTIPLE QUE SE LE HA INDICADO
    def addPreguntaMultiple(self,preguntaMultiple):
        preguntaMultiple.votacionMultiple = self
        preguntaMultiple.save()

class PreguntaMultiple(models.Model):
    id = models.AutoField(primary_key=True)
    votacionMultiple = models.ForeignKey(VotacionMultiple,on_delete = models.CASCADE,related_name="preguntasMultiples")
    textoPregunta = models.CharField(max_length=50)
    def Nombre_VotacionMultiple(self):
        return self.votacionMultiple.titulo
    def __str__(self):
        return self.textoPregunta

    # DEVUELVE EL NÚMERO DE OPCIONES QUE TIENE LA PREGUNTA
    def Numero_De_Opciones(self):
        return OpcionMultiple.objects.filter(preguntaMultiple_id=self.id).count()

    # AÑADE UNA  OPCION MULTIPLE A LA PREGUNTA MULTIPLE
    # A LA HORA DE CREAR LA OPCION MULTIPLE SOLO ES NECESARIO INDICARLE EL ATRIBUTO NOMBRE_OPCION
    # LA FUNCION SE ENCARGA DE ASOCIAR LA OPCION MULTIPLE  A LA PREGUNTA MULTIPLE  QUE SE LE HA INDICADO
    def addOpcionMultiple(self, opcionMultiple):
        opcionMultiple.preguntaMultiple = self
        opcionMultiple.save()

    # DEVUELVE EL Nº DE VECES QUE SE HA VOTADO CADA OPCION QUE TIENE LA PREGUNTA ASOCIADA
    # DEVUELVE UN DICCIONARIO DE LA FORMA:
    # {OPCION1:N_VOTADO,..., OPCION-N: N_VOTAO}
    def cuentaOpcionesMultiple(self):
        opciones = OpcionMultiple.objects.filter(preguntaMultiple_id=self.id).values('nombre_opcion', 'n_votado')
        res = {}
        for opcion in opciones:
            res[opcion['nombre_opcion']] = opcion['n_votado']
        return res

    # SUMA 1 AL CAMPO N_VOTADO DE CADA OPCION QUE SE ENCUENTRE EN EL LISTADO QUE SE LE PASA COMO PARÁMETRO
    def votaOpcioneMultiples(self, listadoOpcionesSeleccionadas):
        for opcion in listadoOpcionesSeleccionadas:
            opcion.preguntaMultiple = self
            opcion.n_votado = opcion.n_votado + 1
            opcion.save()
1
class OpcionMultiple(models.Model):
    id = models.AutoField(primary_key=True)
    preguntaMultiple = models.ForeignKey(PreguntaMultiple,on_delete = models.CASCADE,related_name="opcionesMultiples")
    nombre_opcion = models.CharField(max_length=100)
    n_votado = models.PositiveIntegerField(blank=True, null=True,default=0)

    def __str__(self):
        return self.nombre_opcion
    def Nombre_Pregunta_Multiple(self):
        return self.preguntaMultiple.textoPregunta

#SUMA 1 AL CAMPO N_VOTADO DE LA OPCION SELECCIONADA
    def votaOpciones(self):
        self.n_votado = self.n_votado + 1
        self.save()

#Votaciones Preferencia
class VotacionPreferencia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.titulo

    # DEVUELVE EL NÚMERO DE PREGUNTAS QUE TIENE ASOCIDADA UNA VOTACION DE PREFERENCIA
    def Numero_De_Preguntas_Preferencia(self):
        return PreguntaPreferencia.objects.filter(votacionPreferencia_id=self.id).count()

    # AÑADE UNA PREGUNTA PREFERENCIA  A LA VOTACION PREFERENCIA
    # A LA HORA DE CREAR LA PREGUNTA PREFERENCIA SOLO ES NECESARIO INDICARLE EL ATRIBUTO TEXTOPREGUNTA
     # LA FUNCION SE ENCARGA DE ASOCIAR LA PREGUNTA PREFERENCIA  A LA VOTACION PREFERENCIA QUE SE LE HA INDICADO
    def addPreguntaPreferencia(self, preguntaPreferencia):
        preguntaPreferencia.votacionPreferencia = self
        preguntaPreferencia.save()

class PreguntaPreferencia(models.Model):
    id = models.AutoField(primary_key=True)
    votacionPreferencia = models.ForeignKey(VotacionPreferencia,on_delete = models.CASCADE,related_name="preguntasPreferencia")
    textoPregunta = models.CharField(max_length=50)
    def Nombre_Votacion_Preferencia(self):
        return self.votacionPreferencia.titulo
    def __str__(self):
        return self.textoPregunta

    # DEVUELVE EL NÚMERO DE OPCIONES QUE TIENE LA PREGUNTA
    def Numero_De_Opciones(self):
        return OpcionRespuesta.objects.filter(preguntaPreferencia_id=self.id).count()

    # AÑADE UNA  OPCION RESPUESTA A LA PREGUNTA PREFERENCIA
    # A LA HORA DE CREAR LA OPCION RESPUESTA SOLO ES NECESARIO INDICARLE EL ATRIBUTO NOMBRE_OPCION
    # LA FUNCION SE ENCARGA DE ASOCIAR LA OPCION RESPUESTA  A LA PREGUNTA PREFERENCIA  QUE SE LE HA INDICADO
    def addOpcionRespuesta(self, opcionRespuesta):
        opcionRespuesta.preguntaPreferencia = self
        opcionRespuesta.save()

class OpcionRespuesta(models.Model):
    id = models.AutoField(primary_key=True)
    preguntaPreferencia = models.ForeignKey(PreguntaPreferencia,on_delete = models.CASCADE,related_name="opcionesRespuesta")
    nombre_opcion = models.CharField(max_length=100)
    def Nombre_Pregunta_Preferencia(self):
        return self.preguntaPreferencia.textoPregunta
    def __str__(self):
        return self.nombre_opcion

    # AÑADE UNA  RESPUESTA PREFERENCIA A LA OPCION RESPUESTA
    # A LA HORA DE CREAR LA RESPUESTA PREFERENCIA SOLO ES NECESARIO INDICARLE EL ATRIBUTO ORDEN_PREFERENCIA
    # LA FUNCION SE ENCARGA DE ASOCIAR LA RESPUESTA PREFERENCIA  A LA OPCION RESPUESTA  QUE SE LE HA INDICADO
    def addRespuetaPreferencia(self, respuestaPreferencia):
        respuestaPreferencia.opcionRespuesta = self
        respuestaPreferencia.save()

    # DEVUELVE LA MEDIA DE PREFERENCIA DE LA OPCION EN FUNCION DE LAS RESPUESTAS QUE SE HAN DADO EN ESA OPCION
    def Media_Preferencia(self):
        respuestas = RespuestaPreferencia.objects.filter(opcionRespuesta=self.id).values('orden_preferencia')
        n_respuestas = len(respuestas)
        if n_respuestas == 0:  ##EVITAR DIVISIÓN POR CERO
            n_respuestas = 1
        total = 0
        for value in respuestas:
            total = total + value['orden_preferencia']
        return total / n_respuestas

    # POR CADA OPCION DEVUELVE UN DICCIONARIO CON EL SIGUIENTE FORMATO:
    # (POS1: X veces), (POS2, Y veces),...,(POS N : Z veces)
    # DONDE POS es la posición de preferencia donde se ha puesto dicha opcion y 'X' es el nº de veces que se ha puesto en esa posicion
    def Respuestas_Opcion(self):
        respuestas = RespuestaPreferencia.objects.filter(opcionRespuesta=self.id).values('orden_preferencia')
        result = {}

        for value in respuestas:
            if value['orden_preferencia'] in result:
                result[value['orden_preferencia']] = result[value['orden_preferencia']] + 1
            else:
                result[value['orden_preferencia']] = 1

        for key in result:
            result[key] = str(result[key]) + " veces"

        print(result)
        return sorted(result.items())

class RespuestaPreferencia(models.Model):
    id = models.AutoField(primary_key=True)
    opcionRespuesta = models.ForeignKey(OpcionRespuesta,on_delete = models.CASCADE,related_name="respuestasPreferencia")
    orden_preferencia = models.PositiveIntegerField(blank=True, null=True)
    def Nombre_Opcion_Respuesta(self):
        return self.opcionRespuesta.nombre_opcion

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

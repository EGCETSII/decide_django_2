from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.query_utils import DeferredAttribute
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import validate_comma_separated_integer_list
from datetime import date

from base import mods
from base.models import Auth, Key
from django.contrib.auth.models import User, Group
from store.models import Vote



class Question(models.Model):

    SINGLE_OPTION = 'SO'
    MULTIPLE_CHOICE = 'MC'
    
    TYPES_CHOICES = (
        (SINGLE_OPTION, 'Single_Option'),
        (MULTIPLE_CHOICE, 'Multiple_Choice'),
        
       
    )
    type = models.CharField(
        max_length=2,
        choices=TYPES_CHOICES,
        default=SINGLE_OPTION,
    )
    desc = models.TextField()

    def __str__(self):
        return  '{}'.format(self.desc)


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question, related_name='options', on_delete=models.CASCADE)
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
    question = models.ForeignKey(
        Question, related_name='voting', on_delete=models.CASCADE)

    # Campo groups en votacion
    groups = models.CharField(validators=[
                              validate_comma_separated_integer_list], max_length=200, blank=True, null=True, default='')

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(
        Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    deadline = models.DateField(blank=True, null=True)

    # Comprueba que los grupos indicados en la votacion existen en base de datos

    def clean(self) -> None:
        # Si el grupo es vacío no tengo que comprobar la existencia de los grupos
        if (self.groups != None):
            ids = list(self.groups.split(","))
            for id in ids:
                try:
                    Group.objects.get(pk=int(id))
                except:
                    raise ValidationError('One o more groups do not exist.')

        if self.deadline is not None and self.deadline <= date.today():
            raise ValidationError('Deadline must be in the future.')
        return super().clean()

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [{"name": a.name, "url": a.url} for a in self.auths.all()],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={
                         'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)

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
        data = {"msgs": votes}
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
                votes = tally.count(opt.number) #Recuento de votos
            else:
                votes = 0
            opts.append({
                'option': opt.option,
                'number': opt.number,
                'votes': votes
            })

        data = {'type': 'IDENTITY', 'options': opts}
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name

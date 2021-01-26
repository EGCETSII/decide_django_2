import urllib

from base import mods
from base.models import Auth, Key
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc

class PoliticalParty(models.Model):

    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    leader = models.CharField(max_length=200)
    president = models.CharField(max_length=151, blank=True, null=True)

    def __str__(self):
       return '{} ({}) - {}'.format(self.acronym, self.name, self.leader)

   
    class Meta:
        unique_together = (('name', 'acronym', 'leader'),)



#Añadida clase YesOrNo

class YesOrNoQuestion(models.Model):
    desc = models.TextField()
    CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
        ('M', 'Maybe'),
    )
    choice = models.CharField(max_length=1, choices=CHOICES, blank=True)

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
    political_party = models.ForeignKey(PoliticalParty, related_name='voting', on_delete=models.CASCADE, null=True)
    # ,blank=True

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)
    url = models.CharField(max_length=40, help_text=u"http://localhost:8000/booth/")


    def clean_fields(self, exclude=None):
        super(Voting, self).clean_fields(exclude)
        
        url = urllib.parse.quote_plus(self.url.encode('utf-8'))
        
        if Voting.objects.filter(url=url).exists():
            raise ValidationError({'url': "The url already exists."})

    def save(self, *args, **kwargs):
        try:
            Voting.objects.get(name=self.name)
        except:
            encode_url = urllib.parse.quote_plus(self.url.encode('utf-8'))
            self.url = encode_url
            
        super(Voting, self).save(*args, **kwargs)

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

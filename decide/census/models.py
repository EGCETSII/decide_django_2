from django.db import models
from django.contrib.auth.models import Group, User

class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    adscripcion = models.TextField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

class ParentGroup(Group):
    isPublic = models.BooleanField(default=False)
    voters = models.ManyToManyField(User, blank=True)

class Request(models.Model):
    ACCEPTED = 'ACCEPTED' 
    REJECTED = 'REJECTED'
    PENDING = 'PENDING'
    RequestStatus = ((ACCEPTED, 'ACCEPTED'), (REJECTED, 'REJECTED'), (PENDING, 'PENDING'),)

    voter_id = models.PositiveIntegerField()
    group_id = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=RequestStatus, default=PENDING)
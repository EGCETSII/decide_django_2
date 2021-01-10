from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    VotingTypes = (
        ('VB', 'VotacionBinaria'),
        ('V', 'Votacion'),
        ('VP', 'VotacionPreferencia'),
        ('VM', 'VotacionMultiple'),
        ('Vo', 'Voting'))

    type = models.CharField(max_length=2, choices=VotingTypes, default='Vo')

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

        

    

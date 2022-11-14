from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    #adscripcion_id = models.PositiveIntegerField()
    class Meta:
        #unique_together = (('voting_id', 'voter_id','adscripcion_id'),)
        unique_together = (('voting_id', 'voter_id'),)

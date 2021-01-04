from django.db import models
import ldap3
import re




class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()


    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

        

    

from django.db import models
import ldap3
from .settingsLdap import *
import re




class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

class CensusLdap(models.Model):
    list_key = models.TextField()
    list_value = models.PositiveIntegerField()
    def sacaGrupos(self):
        conn = ldapConnectionMethod('ldap://localhost:389', 'cn=admin,dc=example,dc=com', 'admin')
        uid = '*'
        #search_string='(&(objectclass=person)(uid=%s))' %uid
        conn.search('dc=example,dc=com', '(objectclass=posixGroup)',attributes=['ou'])
        #conn.search('dc={},dc=local'.format('example'), '(objectclass=groups)',attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
        lista = {}
        i=0
        for texto in conn.entries:
            text = str(texto)
            m = re.search('cn=(.+?),', text)
            if m:
                lista[m.group(1)] = i
                i=i+1
        return lista
    listaGrupos = property(sacaGrupos)
    class Meta:
        unique_together = (('list_key', 'list_value'),)

        

    



     

        

            
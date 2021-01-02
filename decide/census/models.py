from django.db import models
import ldap
from settingsLdap import *
from django_auth_ldap.config import LDAPSearch




class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

    class importLdap:
        def sacapropiedades(self):
            conn = ldapConnectionMethod('ldap://localhost:389', 'cn=admin,dc=example,dc=com', 'admin')
            uid = '*'
            search_string='(&(objectclass=person)(uid=%s))' %uid
            conn.search('ou=people,dc=example,dc=com', search_string,attributes=['cn'])
        
            return conn.entries[0]['cn']
        

        

            
"""
from ldap3 import Server, Connection, ALL_ATTRIBUTES
import re
from django.db import models
from ldapMethods import LdapCensus
#from models import Census


#print(Census.objects.get(voting_id=1))
print(LdapCensus().sacaMiembros('ldap://localhost:389','cn=admin,dc=example,dc=com', 'admin',"grupo 4"))
"""
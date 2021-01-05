from ldap3 import Server, Connection, ALL_ATTRIBUTES
import re
from django.db import models
from ldapMethods import LdapCensus
#from models import Census


#print(Census.objects.get(voting_id=1))
#print(LdapCensus().LdapGroups('localhost:389','cn=admin,dc=example,dc=com','admin', 'ou=groups,dc=example,dc=com'))
#print(LdapCensus().LdapMembers('ldap.forumsys.com:389','cn=read-only-admin,dc=example,dc=com', 'ou=scientists,dc=example,dc=com', 'password',"scientists"))
print(LdapCensus().LdapGroups('ldap.forumsys.com:389','cn=read-only-admin,dc=example,dc=com','password', 'ou=chemists,dc=example,dc=com'))

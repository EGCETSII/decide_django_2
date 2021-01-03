from ldap3 import *
from .settingsLdap import ldapConnectionMethod
import re

class importLdap(grupo):

    def sacaGrupos(self, grupo):
        self.grupo = grupo
        conn = ldapConnectionMethod('ldap://localhost:389', 'cn=admin,dc=example,dc=com', 'admin')
        uid = '*'
        search_string='(&(objectclass='+grupo+')(uid=%s))' %uid
        conn.search('dc=example,dc=com', search_string,attributes=[ALL_ATTRIBUTES])
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
    listaGrupos = property(sacaGrupos("grupo 1"))

print(importLdap().listaGrupos)



# found: 1234

# found: 1234


from ldap3 import Server, Connection, ALL_ATTRIBUTES
from settingsLdap import ldapConnectionMethod
import re
from django.db import models

class importLdap:
    
    def sacaGrupos(self, urlLdap, dominio, psw):
        conn = ldapConnectionMethod(urlLdap, dominio, psw)
        #uid = '*'
        #search_string='(&(objectclass=person)(uid=%s))' %uid
        #conn.search('dc={},dc=local'.format('example'), '(objectclass=groups)',attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
        conn.search('dc=example,dc=com', '(objectclass=posixGroup)',attributes=[ALL_ATTRIBUTES])
        lista = {}
        i=0
        for texto in conn.entries:
            text = str(texto)
            grupo = re.search('cn=(.+?),', text)
            gid = re.search('gidNumber: (.+?)\n', text)
            if grupo:
                lista[grupo.group(1)] = gid.group(1)
                i=i+1
        return lista

    def sacaMiembros(self, urlLdap, dominio, psw, grupo):
        conn = ldapConnectionMethod(urlLdap, dominio, psw)
        gidNumber = importLdap().sacaGrupos(urlLdap, dominio, psw)[grupo]
        search_string='(&(objectclass=person)(gidNumber=%s))' %gidNumber
        conn.search('dc=example,dc=com', search_string,attributes=['cn'])
        return conn.entries
  

print(importLdap().sacaMiembros('ldap://localhost:389','cn=admin,dc=example,dc=com', 'admin',"grupo 2"))




    

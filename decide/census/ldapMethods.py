#AUTHENTICATION_BACKENDS = [
#    "django.contrib.auth.backends.ModelBackend",
#    "django_auth_ldap.backend.LDAPBackend",
#]
from ldap3 import Server, Connection
from ldap3 import Server, Connection, ALL_ATTRIBUTES
import re
class LdapCensus:
    def ldapConnectionMethod(self, urlServer, auth, psw):
        server = Server(urlServer)
        conn = Connection(server, auth, psw, auto_bind=True)
        return conn

    def sacaGrupos(self, urlLdap, dominio, psw):
        conn = LdapCensus().ldapConnectionMethod(urlLdap, dominio, psw)
        conn.search('dc=example,dc=com', '(objectclass=posixGroup)',attributes=[ALL_ATTRIBUTES])
        lista = {}
        for texto in conn.entries:
            text = str(texto)
            grupo = re.search('cn=(.+?),', text)
            gid = re.search('gidNumber: (.+?)\n', text)
            if grupo:
                    lista[grupo.group(1)] = gid.group(1)
        return lista

    def sacaMiembros(self, urlLdap, dominio, psw, grupo):
        conn = LdapCensus().ldapConnectionMethod(urlLdap, dominio, psw)
        gidNumber = LdapCensus().sacaGrupos(urlLdap, dominio, psw)[grupo]
        search_string='(&(objectclass=person)(gidNumber=%s))' %gidNumber
        conn.search('dc=example,dc=com', search_string,attributes=[ALL_ATTRIBUTES])
        
        lista = []
        for texto in conn.entries:
            text = str(texto)
            usuario = re.search('uid: (.+?)\n', text)
            if usuario:
                    lista.append(usuario.group(1))
        return lista

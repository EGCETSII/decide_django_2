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

    def LdapGroups(self, LdapUrl, auth, psw, branch):
        conn = LdapCensus().ldapConnectionMethod(LdapUrl, auth, psw)
        conn.search(search_base=branch, search_filter='(objectclass=*)', attributes=[ALL_ATTRIBUTES])
        #conn.search(branch, '(objectclass=posixGroup)',attributes=[ALL_ATTRIBUTES])
        ldapList = []
        print(conn.entries)
        for entries in conn.entries:
            text = str(entries)
            #Si cambias por uid te devuelve los nombres de el grupo que pasas como ou
            group = re.findall('uid=(.+?),', text, re.DOTALL)
            for element in group:
                if group and ldapList.count(element) == 0:            
                    ldapList.append(element)
        return ldapList
    """
    def LdapMembers(self, urlLdap, auth, branch, psw, group):
        conn = LdapCensus().ldapConnectionMethod(urlLdap, auth, psw)
        gidNumber = group
        search_string='(&(objectclass=person)(cn=%s))' %gidNumber
        conn.search(branch, search_string,attributes=[ALL_ATTRIBUTES])
        print(conn.entries)
        ldapList = []
        for entries in conn.entries:
            text = str(entries)
            user = re.search('uid: (.+?)\n', text)
            if user:
                    ldapList.append(user.group(1))
        return ldapList
    """





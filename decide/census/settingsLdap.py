#AUTHENTICATION_BACKENDS = [
#    "django.contrib.auth.backends.ModelBackend",
#    "django_auth_ldap.backend.LDAPBackend",
#]
from ldap3 import Server, Connection


def ldapConnectionMethod(urlServer, auth, psw):
    server = Server(urlServer)
    conn = Connection(server, auth, psw, auto_bind=True)
    return conn



#ldapConnection('ldap://localhost:389', 'cn=admin,dc=example,dc=com', 'admin','ou=people,dc=example,dc=com')

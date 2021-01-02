#AUTHENTICATION_BACKENDS = [
#    "django.contrib.auth.backends.ModelBackend",
#    "django_auth_ldap.backend.LDAPBackend",
#]
from ldap3 import Server, Connection

def ldapConnection(urlServer, auth, psw, tree):
    server = Server(urlServer)
    conn = Connection(server, auth, psw, auto_bind=True)
    uid = '*'
    search_string='(&(objectclass=person)(uid=%s))' %uid
    conn.search(tree, search_string,attributes=['cn'])
    print(conn.entries[0]['cn'])


ldapConnection('ldap://localhost:389', 'cn=admin,dc=example,dc=com', 'admin','ou=people,dc=example,dc=com')

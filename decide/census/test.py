from ldap3 import *
from settingsLdap import ldapConnectionMethod
class importLdap:
    def sacapropiedades(self):
        conn = ldapConnectionMethod('ldap://localhost:389', 'cn=admin,dc=example,dc=com', 'admin')
        uid = '*'
        search_string='(&(objectclass=person)(uid=%s))' %uid
        conn.search('dc=example,dc=com', '(objectclass=posixGroup)',attributes=['ou'])
        #conn.search('dc={},dc=local'.format('example'), '(objectclass=groups)',attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])
        return conn.entries
    bar = property(sacapropiedades)
print(importLdap().bar)

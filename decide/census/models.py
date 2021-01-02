from django.db import models
import ldap
from django_auth_ldap.config import LDAPSearch




class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    


    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

    class modelLdap:

        AUTH_LDAP_SERVER_URI = os.environ.get("ldap://localhost:389")
        AUTH_LDAP_ALWAYS_UPDATE_USER = True
        AUTH_LDAP_BIND_DN = os.environ.get("admin")
        AUTH_LDAP_BIND_PASSWORD = os.environ.get("admin")
        AUTH_LDAP_USER_SEARCH = LDAPSearch(
            "ou=groups,dc=example,dc=com", ldap.SCORE.SUBTREE, "cn=%(user)s"
        )
        AUTH_LDAP_USER_ATTR_MAP = {
            "username": "cn",
           # "first_name": "givenName",
           # "last_name": "sn",
           # "email": "mail",
        }
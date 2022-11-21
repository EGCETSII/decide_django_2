from decide.settings import *
import dj_database_url

# Modules in use, commented modules that you won't use
MODULES = [
    'mixnet',
]

DATABASES = {
    'default': dj_database_url.config(
        engine='django.db.backends.postgresql',
        default='postgres://decide:decide@localhost:5432/decide',
    )
}

BASEURL = 'http://localhost:9000'

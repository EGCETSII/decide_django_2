import dj_database_url

ALLOWED_HOSTS = ['decide.onrender.com', '*']

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]
BASEURL = 'http://decide.onrender.com/'
APIS = {
    'authentication': BASEURL,
    'base': BASEURL,
    'booth': BASEURL,
    'census': BASEURL,
    'mixnet': BASEURL,
    'postproc': BASEURL,
    'store': BASEURL,
    'visualizer': BASEURL,
    'voting': BASEURL,
}

DATABASES = {
    'default': dj_database_url.config(
        engine='django.db.backends.postgresql',
        default='postgres://decide:decide@localhost:5432/decide',
    )
}


# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256

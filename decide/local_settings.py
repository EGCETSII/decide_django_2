BASEURL = 'http://localhost:8000'

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'decide',
        'PASSWORD': 'decide',
        'HOST': '127.0.0.1',
        'PORT': '5432', 
}}

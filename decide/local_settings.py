BASEURL = 'https://decide-production-afa2.up.railway.app'

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
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'LXDIwUYidMB8FTkQyV8g',
        'HOST': 'containers-us-west-152.railway.app',
        'PORT': '5455',
}}

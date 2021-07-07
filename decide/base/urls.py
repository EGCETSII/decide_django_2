from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('i18n/', include('django.conf.urls.i18n')),
]

from django.contrib import admin

from .models import Census
from django.urls import reverse
from django.utils.html import format_html


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )


admin.site.register(Census, CensusAdmin)

from django.contrib import admin

from .models import Census

from .models import CensusLdap


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )
"""
class CensusAdminLdap(admin.ModelAdmin):

    list_display = ('list_key','list_value')
    list_filter = ('list_key', )

    search_fields = ('list_key', )


admin.site.register(CensusLdap, CensusAdminLdap)
"""

admin.site.register(Census, CensusAdmin)
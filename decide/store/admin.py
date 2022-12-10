from django.contrib import admin

from .models import Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id', 'a', 'b')

admin.site.register(Vote, VoteAdmin)

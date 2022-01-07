from django.contrib import admin
from django.contrib.auth.models import User
from .models import Census, ParentGroup, Request

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id', 'adscripcion')
    list_filter = ('voting_id', 'adscripcion')

    search_fields = ('voter_id', )

class ParentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'isPublic')
    list_filter = ('name', 'isPublic')

def accept(modeladmin, request, queryset):
    for v in queryset.all():
        voter = User.objects.get(pk=v.voter_id)
        group = ParentGroup.objects.get(pk=v.group_id)
        if v.status == 'PENDING' and group.isPublic == False:
            group.voters.add(voter)
            v.status = Request.ACCEPTED        
            v.save()
            pending_groups = Request.objects.filter(status='PENDING', voter_id=v.voter_id, group_id=v.group_id)
            for pend_group in pending_groups:
                pend_group.delete()


def reject(modeladmin, request, queryset):
    for v in queryset.all():
        group = ParentGroup.objects.get(pk=v.group_id)
        if v.status == 'PENDING' and group.isPublic == False:
            v.status = Request.REJECTED        
            v.save()
            pending_groups = Request.objects.filter(status='PENDING', voter_id=v.voter_id, group_id=v.group_id)
            for pend_group in pending_groups:
                pend_group.delete()

class RequestAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'group_id', 'request_status')
    list_filter = ('voter_id', 'group_id')

    exclude = ['status']

    search_fields = ('voter_id', 'group_id')

    actions = [ accept, reject]

    def request_status(self, obj):
        return obj.status
           
                    

admin.site.register(Census, CensusAdmin)
admin.site.register(ParentGroup, ParentGroupAdmin)
admin.site.register(Request, RequestAdmin)



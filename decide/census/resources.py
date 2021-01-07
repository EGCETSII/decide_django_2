from import_export import resources
from .models import Census

class CensusResource(resources.ModelResource):
    class Meta:
        model = Census
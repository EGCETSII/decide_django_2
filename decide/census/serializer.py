from rest_framework import serializers
from .models import Census

class CensusSeralizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Census
        fields = '__all__'
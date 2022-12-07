from rest_framework import serializers

from .models import Census


class CensusSerializer(serializers.HyperlinkedModelSerializer):
    voters = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Census
        fields = ('id', 'voting_id', 'voters')

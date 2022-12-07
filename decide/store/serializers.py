from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    opt_number = serializers.IntegerField()
    token = serializers.CharField(max_length=100)
    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id', 'opt_number', 'token')

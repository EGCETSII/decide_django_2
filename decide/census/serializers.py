from rest_framework import serializers

from .models import ParentGroup, Group
from base.serializers import KeySerializer, AuthSerializer


class ParentGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ParentGroup
        fields = ('id', 'name', 'isPublic')


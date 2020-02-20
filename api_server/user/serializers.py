from rest_framework import serializers
from .models import TestModel




class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestModel
        fields = ['name']

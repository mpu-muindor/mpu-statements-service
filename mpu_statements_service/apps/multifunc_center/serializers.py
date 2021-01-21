from rest_framework import serializers
from .models import Blank


class BlankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blank
        fields = ['title', 'blank']

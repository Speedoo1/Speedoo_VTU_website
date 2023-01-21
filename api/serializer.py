from rest_framework import serializers

from index.models import historydata


class historyserilizer(serializers.ModelSerializer):
    class Meta:
        model = historydata
        fields = '__all__'

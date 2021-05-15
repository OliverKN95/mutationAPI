from rest_framework import routers, serializers, viewsets
from .models import logs


class logsSerializer(serializers.ModelSerializer):
    class Meta:
        model = logs
        fields = '__all__'


class hasMutationSerializer(serializers.Serializer):
    """
    Serializer para traer información de estadisticas
    """
    dna = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=100))
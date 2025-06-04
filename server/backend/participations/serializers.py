from rest_framework import serializers
from server.backend.participations.models import Participation

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['id', 'description', 'score', '_class', 'student', 'subject', 'date']   
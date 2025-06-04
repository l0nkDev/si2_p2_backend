from rest_framework import serializers
from server.backend.grades.models import Score, ScoreTarget

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'student', 'target', 'score']        
        
class ScoreTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreTarget
        fields = ['id', 'subject', '_class', 'title', 'trimester']  
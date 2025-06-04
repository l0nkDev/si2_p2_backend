from rest_framework import serializers

from server.backend.assistance.models import Assistance, ClassSession
from server.backend.core.models import Student
from server.backend.core.serializers import StudentSerializer
        
class AssistanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = Assistance
        fields = ['id','status', 'student', 'session'] 
        
class AssistanceSerializerSimple(serializers.ModelSerializer):
    date = serializers.DateField(source='session.date')
    class Meta:
        model = Assistance
        fields = ['id','status', 'date',]  
        
class AssistanceSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Assistance
        fields = ['id','status', 'student', 'session']  
        
class StudentAssistanceSerializer(serializers.ModelSerializer):
    assistances = AssistanceSerializerSimple(many=True)
    class Meta:
        model = Student
        fields = ['id', 'name', 'lname', 'ci', 'rude', 'assistances']  
        
class ClassSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSession
        fields = ['id', '_class', 'subject', 'date', 'status']      
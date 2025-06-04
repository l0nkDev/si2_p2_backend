from rest_framework import serializers
from server.backend.admin.models import Log, Report, fcm

class fcmSerializer(serializers.ModelSerializer):
    class Meta:
        model = fcm
        fields = ['id', 'user', 'token']   
        
class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'user', 'role', 'login', 'action', 'ip', 'time']   
        
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'params', 'title', 'time']   
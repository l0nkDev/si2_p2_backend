from rest_framework import serializers
from server.backend.models import Student, Teacher, User
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'lname', 'ci', 'phone', 'email', 'rude']
            
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'lname', 'ci', 'phone', 'email']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'login', 'password', 'access_token', 'role', 'student', 'teacher']      


'''
class OldStudentSerializer(serializers.Serializer):
    name = serializers.CharField()
    lname = serializers.CharField()
    ci = serializers.IntegerField()
    phone = serializers.IntegerField(required=False)
    email = serializers.CharField(required=False)
    rude = serializers.IntegerField()
    
    def create(self, validated_data):
        return Student.objects.create(validated_data)
    
    def update(self, instance: Student, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.lname = validated_data.get('lname', instance.name)
        instance.ci = validated_data.get('ci', instance.ci)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.rude = validated_data.get('rude', instance.rude)
        instance.save()
        return instance
'''
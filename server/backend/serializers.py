from rest_framework import serializers
from server.backend.models import Assistance, Class, Participation, Score, Student, Subject, Teacher, User
    
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
        
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'score', 'trimester', 'student', 'subject', '_class']    
        
class AssistanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    
    class Meta:
        model = Assistance
        fields = ['id', 'date', 'status', '_class', 'student', 'subject']   
        
class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['id', 'description', 'score', '_class', 'student', 'subject', 'date']   
        
class ClassSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'grade', 'parallel', 'stage', 'year']    
        
class ClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)
    
    class Meta:
        model = Class
        fields = ['id', 'grade', 'parallel', 'stage', 'year', 'students']    
        
class SubjectSerializer(serializers.ModelSerializer):
    classes = ClassSerializerSimple(many=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'title', 'teacher', 'classes']     



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
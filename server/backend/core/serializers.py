from rest_framework import serializers
from server.backend.core.models import Class, Student, Subject, SubjectArea, Teacher, User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'lname', 'ci', 'phone', 'email', 'rude']
            
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'lname', 'ci', 'phone', 'email']
        
class UserSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'login', 'password', 'access_token', 'role', 'student', 'teacher']  
        
class ClassSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'grade', 'parallel', 'stage', 'year']  
         
class SubjectListSerializer(serializers.ModelSerializer):
    classes = ClassSerializerSimple(many=True)
    teacher = TeacherSerializer()
    class Meta:
        model = Subject
        fields = ['id', 'title', 'teacher', 'classes']  
        
class SubjectAreaListSerializer(serializers.ModelSerializer):
    subjects = SubjectListSerializer(many=True)
    class Meta:
        model = SubjectArea
        fields = ['id', 'title', 'subjects']   
        
class SubjectAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectArea
        fields = ['id', 'title']    
        
class ClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)
    class Meta:
        model = Class
        fields = ['id', 'grade', 'parallel', 'stage', 'year', 'students']   
        
class SubjectSerializer(serializers.ModelSerializer):
    classes = ClassSerializerSimple(many=True, read_only=True)
    class Meta:
        model = Subject
        fields = ['id', 'title', 'teacher', 'area', 'classes']   
        
class SubjectSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']  
        
class StudentClassSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializerSimple(many=True)
    class Meta:
        model = Class
        fields = ['id', 'grade', 'parallel', 'stage', 'year', 'subjects']   
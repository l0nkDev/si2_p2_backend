from rest_framework import serializers
from server.backend.models import Assistance, Class, ClassSession, Participation, Score, ScoreTarget, Student, Subject, SubjectArea, Teacher, User
    
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
        fields = ['id', 'student', 'target', 'score']    
        
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
        
class ClassSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'grade', 'parallel', 'stage', 'year']     
        
class SubjectSerializer(serializers.ModelSerializer):
    classes = ClassSerializerSimple(many=True)
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
        
#----------------------------SUBJECT AREA--------------------------------------------

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
        
#---------------------------------------------------------------------------- 
        
class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['id', 'description', 'score', '_class', 'student', 'subject', 'date']   
        
class ClassSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)
    class Meta:
        model = Class
        fields = ['id', 'grade', 'parallel', 'stage', 'year', 'students']        
        
class ClassSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSession
        fields = ['id', '_class', 'subject', 'date', 'status']        
        
class ScoreTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreTarget
        fields = ['id', 'subject', '_class', 'title', 'trimester']   

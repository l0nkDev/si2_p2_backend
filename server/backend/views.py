from server.backend.models import Assistance, Class, Participation, Score, Student, Subject, Teacher, User
from server.backend.serializers import AssistanceSerializer, ParticipationSerializer, ScoreSerializer, StudentSerializer, SubjectSerializer, TeacherSerializer, UserSerializer
from server.backend.permissions import IsLoggedIn, IsAdmin, IsStudent, IsTeacher
from rest_framework import generics, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from secrets import token_urlsafe

class StudentList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User()
            user.access_token = token_urlsafe()
            user.login = request.data['rude']
            user.password = request.data['ci']
            user.role = 'S'
            user.student = Student.objects.get(pk=serializer.data["id"])
            user.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TeacherList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, format=None):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User()
            user.access_token = token_urlsafe()
            user.login = request.data['email']
            user.password = request.data['ci']
            user.role = 'T'
            user.teacher = Teacher.objects.get(pk=serializer.data["id"])
            user.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserSelf(APIView):
    permission_classes = [IsLoggedIn]
    def get(self, request, format=None):
        print(request.META['HTTP_AUTHORIZATION'])
        try: 
            user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
        except: 
            return Response(status=406)
        if user != None: 
            return Response(UserSerializer(user).data)
        return Response(status=400)
    
class UserLogin(APIView):
    def post(self, request, format=None):
        try: 
            user = User.objects.get(login=request.data['login'], password=request.data['password'])
        except: 
            return Response(status=406)
        if user != None: 
            return Response(UserSerializer(user).data)
        return Response(status=400)

class CreateClassesForYear(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, format=None):
        tmp = Class.objects.filter(year=request.data['year']).first()
        if (tmp != None): return Response({"detail": "Year already created."}, status=400)
        parallels = ['A', 'B', 'C']
        stages = ['P', 'S']
        for stage in stages:
            for i in range(6):
                for parallel in parallels:
                    c = Class()
                    c.grade = i+1
                    c.parallel = parallel
                    c.stage = stage
                    c.year = request.data['year']
                    c.save()
        return Response(status=200)  
    
class ScoreList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    
class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer  
      
class AssistanceList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Assistance.objects.all()
    serializer_class = AssistanceSerializer
    
class AssistanceDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Assistance.objects.all()
    serializer_class = AssistanceSerializer
      
class ParticipationList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    
class ParticipationDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

class TeachersClasses(APIView):
    #permission_classes = [IsTeacher]
    def get(self, request, format=None):
        year = None
        try: year = request.data['year']
        except: year = 2025
        subjects = Subject.objects.filter(teacher=User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).teacher)
        serializer = SubjectSerializer(data=subjects, many=True)
        if serializer.is_valid():
            ''
        return Response(serializer.data, status=200)
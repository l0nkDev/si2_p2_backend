import zoneinfo
from server.backend.models import Assistance, Class, ClassSession, Participation, Score, ScoreTarget, Student, Subject, SubjectArea, Teacher, User
from server.backend.serializers import AssistanceSerializer, AssistanceSerializerSimple, AssistanceSerializerUpdate, ClassSerializerSimple, ClassSessionSerializer, ParticipationSerializer, ScoreSerializer, ScoreTargetSerializer, StudentAssistanceSerializer, StudentClassSerializer, StudentSerializer, SubjectAreaListSerializer, SubjectAreaSerializer, SubjectSerializer, SubjectSerializerSimple, TeacherSerializer, UserSerializer
from server.backend.permissions import IsLoggedIn, IsAdmin, IsStudent, IsTeacher
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
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

class AssignClassSubject(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, pk, format=None):
        c = Class.objects.get(pk=request.data['class'])
        c.subjects.add(Subject.objects.get(pk=pk))
        c.save()
        return Response(status=200)  
    
class ScoreList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    
class ClassList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Class.objects.all().order_by('stage', 'grade', 'parallel')
    serializer_class = ClassSerializerSimple
    
class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer  
    
class SubjectAreaList(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = SubjectArea.objects.all().order_by('title')
    serializer_class = SubjectAreaListSerializer
    
class SubjectList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Subject.objects.all().order_by('title')
    serializer_class = SubjectSerializer
    
class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer  
      
class AssistanceList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Assistance.objects.all()
    serializer_class = AssistanceSerializerUpdate
    
class AssistanceDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Assistance.objects.all()
    serializer_class = AssistanceSerializerUpdate
      
class ParticipationList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    
class ClassSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
      
class ClassSessionList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
    
class ParticipationDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

class TeachersClasses(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, format=None):
        year = None
        try: year = request.data['year']
        except: year = 2025
        subjects = Subject.objects.filter(teacher=User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).teacher)
        serializer = SubjectSerializer(data=subjects, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)

class StudentsClasses(APIView):
    permission_classes = [IsStudent]
    def get(self, request, format=None):
        student = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).student
        print(student)
        year = None
        try: year = request.data['year']
        except: year = 2025
        _class = Class.objects.get(year=year, students=student)
        return Response(StudentClassSerializer(_class).data, status=200)
        
class ClassAssistance(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, pk, _class, format=None):
        students = Class.objects.get(pk=_class).students.order_by('lname', 'name')
        serializer = StudentAssistanceSerializer(data=students, many=True)
        serializer.is_valid()
        students = serializer.data
        for student in students:
            assistances = Assistance.objects.filter(session__subject__id= pk, student__id = student['id'])
            a = AssistanceSerializerSimple(data=assistances, many=True)
            a.is_valid()
            a = a.data
            student['assistances'] = a
        return Response(students, status=200)
        
class ClassAssistanceStudent(APIView):
    permission_classes = [IsStudent]
    def get(self, request, pk, _class, format=None):
        students = Class.objects.get(pk=_class).students.order_by('lname', 'name')
        serializer = StudentAssistanceSerializer(data=students, many=True)
        serializer.is_valid()
        students = serializer.data
        for student in students:
            assistances = Assistance.objects.filter(session__subject__id= pk, student__id = student['id'])
            a = AssistanceSerializerSimple(data=assistances, many=True)
            a.is_valid()
            a = a.data
            student['assistances'] = a
        return Response(students, status=200)

class AreaList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = SubjectArea.objects.all()
    serializer_class = SubjectAreaSerializer
    
class TeachersSessions(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, pk, _class, format=None):
        sessions = ClassSession.objects.filter(_class__id=_class, subject__id=pk)
        serializer = ClassSessionSerializer(data=sessions, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)
    
class StudentsSessions(APIView):
    permission_classes = [IsStudent]
    def get(self, request, pk, _class, format=None):
        sessions = ClassSession.objects.filter(_class__id=_class, subject__id=pk)
        serializer = ClassSessionSerializer(data=sessions, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=200)
    
class StudentSessionStatus(APIView):
    permission_classes = [IsStudent]
    def get(self, request, pk, _class, format=None):
        print(timezone.now().today())
        try: 
            c = ClassSession.objects.get(subject=pk, _class=_class, date=timezone.now().today())
            cs = ClassSessionSerializer(c)
            return Response(cs.data, status=200)
        except:
            return Response({"detail": "class hasn't started yet"}, 200)
        
    def post(self, request, pk, _class, format=None):
        s = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).student
        c = ClassSession.objects.get(subject=pk, _class=_class, date=timezone.now().today())
        try:
            a = Assistance.objects.get(student=s, session=c)
        except:
            a = Assistance()
            a.student = s
            a.session = c
        if c.status == 'S': a.status = 'present'
        if c.status == 'E': a.status = 'missed'
        if c.status == 'L': a.status = 'late'
        a.save()
        return Response(status=200)
    
    
class TeacherSessionStatus(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, pk, _class, format=None):
        print(timezone.now().today())
        try: 
            c = ClassSession.objects.get(subject=pk, _class=_class, date=timezone.now().today())
            cs = ClassSessionSerializer(c)
            return Response(cs.data, status=200)
        except:
            return Response({"detail": "class hasn't started yet"}, 200)
        
    def post(self, request, pk, _class, format=None):
        print(timezone.now().today())
        try: 
            c = ClassSession.objects.get(subject=pk, _class=_class, date=timezone.now().today())
            c.status = request.data['status']
            c.save()
            cs = ClassSessionSerializer(c)
            return Response(cs.data, status=200)
        except:
            c = ClassSession()
            c._class = Class.objects.get(pk=_class)
            c.subject = Subject.objects.get(pk=pk)
            c.status = request.data['status']
            c.date = timezone.now().today()
            c.save()
            cs = ClassSessionSerializer(c)
            return Response(cs.data, status=200)
        
class ClassParticipation(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, pk, _class, format=None):
        students = Class.objects.get(pk=_class).students.order_by('lname', 'name')
        s = StudentSerializer(data=students, many=True)
        s.is_valid()
        students = s.data
        for student in students:
            participations = Participation.objects.filter(subject__id=pk, _class__id=_class, student__id=student['id']).order_by('id')
            p = ParticipationSerializer(data=participations, many=True)
            p.is_valid()
            participations = p.data
            student['participations'] = participations
        return Response(students, status=200)
    
    def post(self, request, pk, _class, format=None):
        participation = Participation()
        participation.description = request.data["description"]
        participation.score = request.data["score"]
        participation.student = Student.objects.get(pk=request.data["student"])
        participation._class =Class.objects.get(pk=_class)
        participation.subject =Subject.objects.get(pk=pk)
        participation.date = timezone.now().today()
        participation.save()
        serializer = ParticipationSerializer(data=participation)
        serializer.is_valid()
        return Response(serializer.data, status=200)
    
    def put(self, request, pk, _class, format=None):
        participation = Participation.objects.get(pk=request.data['id'])
        participation.description = request.data["description"]
        participation.score = request.data["score"]
        participation.save()
        serializer = ParticipationSerializer(data=participation)
        serializer.is_valid()
        return Response(serializer.data, status=200)
    
    def patch(self, request, pk, _class, format=None):
        participation = Participation.objects.get(pk=request.data['id'])
        participation.delete()
        return Response(status=200)

class StudentParticipation(APIView):
    permission_classes = [IsStudent]
    def get(self, request, pk, _class, format=None):
        student = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).student
        s = StudentSerializer(student)
        student = s.data
        participations = Participation.objects.filter(subject__id=pk, _class__id=_class, student__id=student['id']).order_by('id')
        p = ParticipationSerializer(data=participations, many=True)
        p.is_valid()
        participations = p.data
        student['participations'] = participations
        return Response(student, status=200)
    
class ClassScoreTargets(APIView):
    permission_classes= [IsTeacher]
    def get(self, request, pk, _class, format=None):
        targets = ScoreTarget.objects.filter(_class__id=_class, subject__id=pk)
        s = ScoreTargetSerializer(data=targets, many=True)
        s.is_valid()
        targets = s.data
        return Response(targets, status=200)
    
    def post(self, request, pk, _class, format=None):
        target = ScoreTarget()
        target.subject = Subject.objects.get(pk=pk)
        target._class = Class.objects.get(pk=_class)
        target.title = request.data['title']
        target.trimester = request.data['trimester']
        s = ScoreTargetSerializer(target)
        target = s.data
        return Response(target, status=200)
        
    
class ClassScores(APIView):
    permission_classes= [IsTeacher]
    def get(self, request, pk, _class, format=None):
        students = Class.objects.get(pk=_class).students.order_by('lname', 'name')
        s = StudentSerializer(data=students, many=True)
        s.is_valid()
        students = s.data
        for student in students:
            targets = ScoreTarget.objects.filter(_class__id=_class, subject__id=pk)
            scores = Score.objects.filter(student__id=student['id'], target__in=targets)
            s = ScoreSerializer(data=scores, many=True)
            s.is_valid()
            scores = s.data
            student['scores'] = scores
        return Response(students, status=200)
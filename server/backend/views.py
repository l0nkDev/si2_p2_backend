import json
import zoneinfo

import requests
from server.backend.models import Log, Assistance, Class, ClassSession, Participation, Score, ScoreTarget, Student, Subject, SubjectArea, Teacher, User, fcm
from server.backend.serializers import AssistanceSerializer, AssistanceSerializerSimple, AssistanceSerializerUpdate, ClassSerializerSimple, ClassSessionSerializer, LogSerializer, ParticipationSerializer, ScoreSerializer, ScoreTargetSerializer, StudentAssistanceSerializer, StudentClassSerializer, StudentSerializer, SubjectAreaListSerializer, SubjectAreaSerializer, SubjectSerializer, SubjectSerializerSimple, TeacherSerializer, UserSerializer, fcmSerializer
from server.backend.permissions import IsLoggedIn, IsAdmin, IsStudent, IsTeacher
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from google.oauth2 import service_account
import google.auth.transport.requests
from secrets import token_urlsafe

service_account_file = './si2-p1-mobile-firebase-adminsdk-fbsvc-c39d103571.json'
credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=['https://www.googleapis.com/auth/cloud-platform'])

def get_access_token():
    print('reached get_access_token()')
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    print('finished get_access_token()')
    return credentials.token

def send_fcm_notification(device_token, title, body):
    print('reached send_fcm_notification()')
    fcm_url = 'https://fcm.googleapis.com/v1/projects/si2-p1-mobile/messages:send'
    message = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }
    headers = {
        'Authorization': f'Bearer {get_access_token()}',
        'Content-Type': 'application/json; UTF-8'
    }
    response = requests.post(fcm_url, headers=headers, data=json.dumps(message))
    print('finished send_fcm_notification()')
    if response.status_code == 200:
        print('Notification sent!')
    else:
        print(f"Error sending notification: {response.status_code}, {response.text}")
        
def saveLog(request, action): 
    log = Log()
    user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
    if user.role == 'S':
        log.user = user.student.lname + " " + user.student.name
    if user.role == 'T':
        log.user = user.teacher.lname + " " + user.teacher.name
    if user.role == 'A':
        log.user = user.login
    log.role = user.role
    log.login = user.login
    log.action = action
    log.ip = request.META['REMOTE_ADDR']
    log.time = timezone.now().today()
    log.save()
        
def saveLogUser(request, action, user): 
    log = Log()
    if user.role == 'S':
        log.user = user.student.lname + " " + user.student.name
    if user.role == 'T':
        log.user = user.teacher.lname + " " + user.teacher.name
    if user.role == 'A':
        log.user = user.login
    log.role = user.role
    log.login = user.login
    log.action = action
    log.ip = request.META['REMOTE_ADDR']
    log.time = timezone.now().today()
    log.save()

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
            if user.role == 'S':
                try:
                    token = request.data['fcm']
                    f = fcm()
                    f.user = user
                    f.token = token
                    f.save()
                except: ''
        except: 
            return Response(status=406)
        if user != None: 
            saveLogUser(request, 'Inició sesión', user)
            return Response(UserSerializer(user).data)
        return Response(status=400)
    
class UserLogout(APIView):
    def post(self, request, format=None):
        try: 
            user = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1])
            if user.role == 'S':
                try:
                    token = request.data['fcm']
                    f = fcm.objects.get(user=user, token=token)
                    f.delete()
                except: ''
        except: 
            return Response(status=406)
        if user != None: 
            saveLog(request, 'Cerró sesión')
            return Response(status=200)
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
        student = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).student
        serializer = StudentAssistanceSerializer(student)
        student = serializer.data
        assistances = Assistance.objects.filter(session__subject__id= pk, student__id = student['id'])
        a = AssistanceSerializerSimple(data=assistances, many=True)
        a.is_valid()
        a = a.data
        student['assistances'] = a
        return Response(student, status=200)

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
        target.save()
        s = ScoreTargetSerializer(target)
        target = s.data
        return Response(target, status=200)
    
    def put(self, request, pk, _class, format=None):
        target = ScoreTarget.objects.get(pk=request.data['id'])
        target.title = request.data['title']
        target.save()
        s = ScoreTargetSerializer(target)
        target = s.data
        return Response(target, status=200)
    
    def patch(self, request, pk, _class, format=None):
        target = ScoreTarget.objects.get(pk=request.data['id'])
        target.delete()
        return Response(status=200)
        
    
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
    
    def post(self, request, pk, _class, format=None):
        try:
            score = Score.objects.get(student__id=request.data['student'], target__id=request.data['target'])
        except:
            score = Score()
            score.student = Student.objects.get(pk=request.data['student'])
            score.target = ScoreTarget.objects.get(pk=request.data['target'])
        score.score = request.data['score']
        score.save()
        s = ScoreSerializer(score)
        fcms = fcm.objects.filter(user__student__id = request.data['student'])
        fs = fcmSerializer(data=fcms, many=True)
        fs.is_valid()
        fcms = fs.data
        for f in fcms:
            send_fcm_notification(f['token'], 'Notas de ' + score.target.subject.title + ' actualizadas!', 'Sacaste ' + str(score.score) + ' en ' + score.target.title)
        return Response(s.data, status=200)
    
class StudentScoreTargets(APIView):
    permission_classes= [IsStudent]
    def get(self, request, pk, _class, format=None):
        targets = ScoreTarget.objects.filter(_class__id=_class, subject__id=pk)
        s = ScoreTargetSerializer(data=targets, many=True)
        s.is_valid()
        targets = s.data
        return Response(targets, status=200) 
    
class StudentScores(APIView):
    permission_classes= [IsStudent]
    def get(self, request, pk, _class, format=None):
        student = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).student
        s = StudentSerializer(student)
        student = s.data
        targets = ScoreTarget.objects.filter(_class__id=_class, subject__id=pk)
        scores = Score.objects.filter(student__id=student['id'], target__in=targets)
        s = ScoreSerializer(data=scores, many=True)
        s.is_valid()
        scores = s.data
        student['scores'] = scores
        return Response(student, status=200)    
    
class LogsList(APIView):
    permission_classes= [IsAdmin]
    def get(self, request, format=None):
        try: page = int(request.query_params['page'])
        except: page = 0
        logs = Log.objects.all().order_by('-id')[(20*page):(20*page)+20]
        s = LogSerializer(data=logs, many=True)
        s.is_valid()
        return Response(s.data, status=200)


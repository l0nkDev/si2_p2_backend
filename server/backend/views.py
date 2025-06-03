from cmath import sqrt
from datetime import time
import datetime
import io
import json
from time import mktime
import zoneinfo

import requests
from reportehelper import reportes
from server.backend.models import Log, Assistance, Class, ClassSession, Participation, Report, Score, ScoreTarget, Student, Subject, SubjectArea, Teacher, User, fcm
from server.backend.serializers import AssistanceSerializer, AssistanceSerializerSimple, AssistanceSerializerUpdate, ClassSerializerSimple, ClassSessionSerializer, LogSerializer, ParticipationSerializer, ReportSerializer, ScoreSerializer, ScoreTargetSerializer, StudentAssistanceSerializer, StudentClassSerializer, StudentSerializer, SubjectAreaListSerializer, SubjectAreaSerializer, SubjectSerializer, SubjectSerializerSimple, TeacherSerializer, UserSerializer, fcmSerializer
from server.backend.permissions import IsLoggedIn, IsAdmin, IsStudent, IsTeacher
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from google.oauth2 import service_account
import google.auth.transport.requests
from django.core.management import call_command
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
    
def subjectPrediction(subject, _class, student):
    targets = ScoreTarget.objects.filter(_class=_class, subject=subject)
    scores = Score.objects.filter(student=student, target__in=targets)
    s = ScoreSerializer(data=scores, many=True)
    s.is_valid()
    scores = s.data
    sumx = 0
    sumy = 0
    sumxy = 0
    sumx2 = 0
    sumy2 = 0
    n = len(scores)
    for score in scores:
        x = (mktime(ScoreTarget.objects.get(pk=score['target']).date.timetuple())/86400) - 19500
        y = score['score']
        print(x)
        print(y)
        sumy += y
        sumx += x
        sumxy += x*y
        sumx2 += pow(x, 2)
        sumy2 += pow(y, 2)
    b = ((sumx*sumy)-(n*sumxy))/(-(n*sumx2)+pow(sumx, 2))
    a = (sumy-(b*sumx))/n
    print(a)
    print(b)
        
    
    return Response(student, status=200) 
    

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
        saveLog(request, 'Asignó ' + Subject.objects.get(pk=pk).title + ' a ' + c.stage + str(c.grade) + c.parallel)
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
        saveLog(request, 'Marcó asistencia en ' + a.session.subject.title)
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
            saveLog(request, 'Actualizó su clase de ' + c.subject.title)
            return Response(cs.data, status=200)
        except:
            c = ClassSession()
            c._class = Class.objects.get(pk=_class)
            c.subject = Subject.objects.get(pk=pk)
            c.status = request.data['status']
            c.date = timezone.now().today().date()
            c.save()
            cs = ClassSessionSerializer(c)
            saveLog(request, 'Actualizó su clase de ' + c.subject.title)
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
        saveLog(request, 'Creó una participación de ' + participation.student.lname + ' ' + participation.student.name + ' en la materia ' + participation.subject.title)
        return Response(serializer.data, status=200)
    
    def put(self, request, pk, _class, format=None):
        participation = Participation.objects.get(pk=request.data['id'])
        participation.description = request.data["description"]
        participation.score = request.data["score"]
        participation.save()
        serializer = ParticipationSerializer(data=participation)
        serializer.is_valid()
        saveLog(request, 'Actualizó una participación de ' + participation.student.lname + ' ' + participation.student.name + ' en la materia ' + participation.subject.title)
        return Response(serializer.data, status=200)
    
    def patch(self, request, pk, _class, format=None):
        participation = Participation.objects.get(pk=request.data['id'])
        saveLog(request, 'Eliminó una participación de ' + participation.student.lname + ' ' + participation.student.name + ' en la materia ' + participation.subject.title)
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
        target.date = timezone.now().today()
        target.save()
        s = ScoreTargetSerializer(target)
        saveLog(request, 'Creó una entrada de notas de la materia ' + target.subject.title)
        target = s.data
        return Response(target, status=200)
    
    def put(self, request, pk, _class, format=None):
        target = ScoreTarget.objects.get(pk=request.data['id'])
        target.title = request.data['title']
        target.save()
        s = ScoreTargetSerializer(target)
        saveLog(request, 'Actualizó una entrada de notas de la materia ' + target.subject.title)
        target = s.data
        return Response(target, status=200)
    
    def patch(self, request, pk, _class, format=None):
        target = ScoreTarget.objects.get(pk=request.data['id'])
        saveLog(request, 'Eliminó una entrada de notas de la materia ' + target.subject.title)
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
        saveLog(request, 'Actualizó las notas de la materia ' + score.target.title)
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
    
class BackupsList(APIView):
    permission_classes= [IsAdmin]
    def get(self, request, format=None):
        l = ['test']
        with io.StringIO() as f:
            call_command('listbackups', stdout=f)
            l = f.getvalue().splitlines()
        response = []
        for line in l:
            t = line.split()
            if len(t) == 3:
                response.append({"name": t[0], "date": t[1], "time": t[2]})
        response.reverse()
        return Response(response ,status=200)
    
    def post(self, request, format=None):
        saveLog(request, 'Generó una copia de seguridad')
        call_command('dbbackup')
        return Response(status=200)
    
    def put(self, request, format=None):
        call_command('dbrestore', '--noinput', '-i' + request.data['name'])
        saveLog(request, 'Restauró una copia de seguridad')
        return Response(status=200)
    
class ReporteShow(APIView):
    def get(self, request, format=None):
        if (request.query_params['type'] == 'logs'):
            role = request.query_params['role']
            since = request.query_params['since']
            until = request.query_params['until']
            l = Log.objects.all()
            if since == 'any' and until != 'any':
                l = l.filter(time__lte=until)
            if since != 'any' and until == 'any':
                l = l.filter(time__gte=since)
            if since != 'any' and until != 'any':
                l = l.filter(time__range=[since, until])
            if role != 'any':
                l = l.filter(role=role)
            s = LogSerializer(data=l, many=True)
            s.is_valid()
            s = s.data
            r = []
            for e in s:
                r.append([e['id'], e['user'], e['login'], e['role'], e['action'], e['ip'], e['time']])
            return reportes('BITÁCORA', r, ['id', 'Usuario', 'Login', 'Rol', 'Acción', 'IP', 'Fecha y hora'], request.query_params['f'])
        
        if (request.query_params['type'] == 'teachers'):
            t = Teacher.objects.all()
            s = TeacherSerializer(data=t, many=True)
            s.is_valid()
            t = s.data
            r = []
            for e in t:
                r.append([e['id'], e['lname'], e['name'], e['ci'], e['phone'], e['email']])
            return reportes('DOCENTES', r, ['id', 'Apellido(s)', 'Nombre(s)', 'Cédula de identidad', 'Teléfono', 'Correo electrónico'], request.query_params['f'])
        
        if (request.query_params['type'] == 'students'):
            t = Student.objects.all()
            s = StudentSerializer(data=t, many=True)
            s.is_valid()
            t = s.data
            r = []
            for e in t:
                r.append([e['id'], e['lname'], e['name'], e['ci'], e['phone'], e['email'], e['rude']])
            return reportes('ESTUDIANTES', r, ['id', 'Apellido(s)', 'Nombre(s)', 'Cédula de identidad', 'Teléfono', 'Correo electrónico', 'RUDE'], request.query_params['f'])
            
        return Response(status=400)
    
class ReporteList(APIView):
    permission_classes = [IsAdmin]
    def get(self, request, format=None):
        subjectPrediction( Subject.objects.get(pk=1), Class.objects.get(pk=253), Student.objects.get(pk=2))
        r = Report.objects.all().order_by('-time')
        s = ReportSerializer(data=r, many=True)
        s.is_valid()
        r = s.data
        return Response(r, status=200)
    
    def post(self, request, format=None):
        r = Report()
        r.params = request.data['params']
        r.title = request.data['title']
        r.time = timezone.now().today()
        r.save()
        saveLog(request, 'Generó un reporte de ' + r.title)
        return Response(status=200)
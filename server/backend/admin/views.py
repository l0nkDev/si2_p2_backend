from django.utils import timezone
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from reportehelper import reportes
from server.backend.admin.models import Log, Report
from server.backend.admin.serializers import LogSerializer, ReportSerializer
from server.backend.core.models import Class, Student, Subject, Teacher
from server.backend.core.serializers import StudentSerializer, TeacherSerializer
from server.backend.permissions import IsAdmin
from si2p2utils import saveLog, subjectPrediction
from django.core.management import call_command
    
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
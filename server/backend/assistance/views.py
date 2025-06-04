
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from server.backend.assistance.models import Assistance, ClassSession
from server.backend.assistance.serializers import AssistanceSerializerSimple, AssistanceSerializerUpdate, ClassSessionSerializer, StudentAssistanceSerializer
from server.backend.core.models import Class, Subject, User
from server.backend.permissions import IsStudent, IsTeacher
from si2p2utils import saveLog

class AssistanceList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Assistance.objects.all()
    serializer_class = AssistanceSerializerUpdate
    
class AssistanceDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Assistance.objects.all()
    serializer_class = AssistanceSerializerUpdate
    
class ClassSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
      
class ClassSessionList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
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
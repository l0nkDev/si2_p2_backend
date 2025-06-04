from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from server.backend.core.models import Class, Student, Subject, User
from server.backend.core.serializers import StudentSerializer
from server.backend.participations.models import Participation
from server.backend.participations.serializers import ParticipationSerializer
from server.backend.permissions import IsStudent, IsTeacher
from si2p2utils import saveLog

class ParticipationList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    
class ParticipationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTeacher]
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
        
        
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
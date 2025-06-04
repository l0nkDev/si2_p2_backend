from django.utils import timezone
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from server.backend.admin.models import fcm
from server.backend.admin.serializers import fcmSerializer
from server.backend.core.models import Class, Student, Subject, User
from server.backend.core.serializers import StudentSerializer
from server.backend.grades.models import Score, ScoreTarget
from server.backend.grades.serializers import ScoreSerializer, ScoreTargetSerializer
from server.backend.permissions import IsStudent, IsTeacher
from si2p2utils import saveLog, send_fcm_notification, subjectPrediction

class ScoreList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    
class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [IsAdmin]
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer 
     
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
        st = Student.objects.get(pk=request.data['student'])
        sct = ScoreTarget.objects.get(pk=request.data['target'])
        pred = subjectPrediction(sct.subject, sct._class, st)['prediction']
        if pred < 51:
            send_mail( "NOTIFICACION DE BAJO RENDIMIENTO", "El estudiante " + st.lname + " " + st.name + " está en peligro de reprobar " + sct.subject.title + ". Se prevé que saque alrededor de un " + str(pred) + ".", "l0nkdev@gmail.com", [st.email], fail_silently=True)
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
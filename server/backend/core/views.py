from secrets import token_urlsafe
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins
from server.backend.admin.models import fcm
from server.backend.core.models import Class, Student, Subject, SubjectArea, Teacher, User
from server.backend.core.serializers import ClassSerializerSimple, StudentClassSerializer, StudentSerializer, SubjectAreaListSerializer, SubjectAreaSerializer, SubjectSerializer, TeacherSerializer, UserSerializer
from server.backend.permissions import IsAdmin, IsLoggedIn, IsStudent, IsTeacher
from si2p2utils import saveLog, saveLogUser, subjectPrediction

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
    permission_classes = [IsAdmin]
    queryset = Teacher.objects.all().order_by('lname', 'name')
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
    
class CreateUser(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, format=None):
        u = User()
        u.role = 'A'
        u.login = request.data['login']
        u.password = request.data['password']
        u.access_token = token_urlsafe()
        u.save()
        return Response(status=200)
    
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

class AssignClassSubject(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, pk, format=None):
        c = Class.objects.get(pk=request.data['class'])
        c.subjects.add(Subject.objects.get(pk=pk))
        c.save()
        saveLog(request, 'Asignó ' + Subject.objects.get(pk=pk).title + ' a ' + c.stage + str(c.grade) + c.parallel)
        return Response(status=200) 
    
class ClassList(generics.ListCreateAPIView):
    #permission_classes = [IsAdmin]
    queryset = Class.objects.all().order_by('stage', 'grade', 'parallel')
    serializer_class = ClassSerializerSimple
    
class SubjectAreaList(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = SubjectArea.objects.all().order_by('title')
    serializer_class = SubjectAreaListSerializer
    
class SubjectList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Subject.objects.all().order_by('title')
    serializer_class = SubjectSerializer
    
class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer  

class TeachersClasses(APIView):
    permission_classes = [IsTeacher]
    def get(self, request, format=None):
        year = None
        try: year = request.data['year']
        except: year = 2025
        subjects = Subject.objects.filter(teacher=User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).teacher)
        serializer = SubjectSerializer(data=subjects, many=True)
        serializer.is_valid()
        subs = serializer.data
        for sub in subs:
            for cl in sub['classes']:
                stu = Class.objects.get(pk=cl['id']).students
                ss = StudentSerializer(data=stu, many=True)
                ss.is_valid()
                students = ss.data
                for student in students:
                    student['scores'] = subjectPrediction(Subject.objects.get(pk=sub['id']), Class.objects.get(pk=cl['id']), Student.objects.get(pk=student['id']))
                cl['students'] = students
        return Response(subs, status=200)

class StudentsClasses(APIView):
    permission_classes = [IsStudent]
    def get(self, request, format=None):
        student = User.objects.get(access_token=request.META['HTTP_AUTHORIZATION'].split()[1]).student
        print(student)
        year = None
        try: year = request.data['year']
        except: year = 2025
        _class = Class.objects.get(year=year, students=student)
        cl = StudentClassSerializer(_class).data
        for c in cl['subjects']:
            c['scores'] = subjectPrediction(Subject.objects.get(pk=c['id']), _class, student)
        return Response(cl, status=200)

class AreaList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = SubjectArea.objects.all()
    serializer_class = SubjectAreaSerializer
    
class StudentProfile(APIView): 
    def get(self, request, pk, format=None):
        student = Student.objects.get(pk=pk)
        st = StudentSerializer(student).data
        _class = Class.objects.get(year=2025, students=student)
        cl = StudentClassSerializer(_class).data
        for c in cl['subjects']:
            c['scores'] = subjectPrediction(Subject.objects.get(pk=c['id']), _class, student)
        st['classes'] = cl
        return Response(st, status=200)
    

class AssignUserClass(APIView):
    permission_classes = [IsAdmin]
    def post(self, request, pk, format=None):
        c = Class.objects.get(pk=request.data['class'])
        s = Student.objects.get(pk=request.data['student'])
        s.classes.clear()
        s.classes.add(c)
        s.save()
        return Response(status=200)
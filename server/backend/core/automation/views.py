import random
from secrets import token_urlsafe
from rest_framework.response import Response
from rest_framework.views import APIView

from server.backend.core.models import Class, Student, Subject, Teacher, User
from server.backend.core.serializers import StudentSerializer, SubjectSerializerSimple
from server.backend.grades.models import Score, ScoreTarget

names = ['Santiago', 'Diego', 'Mateo', 'Jose', 'Iván', 'Sebastián', 'Camilo', 'Leonardo', 
         'Iker', 'Matías', 'Dominic', 'José', 'Teotriste', 'Luis', 'Abalgamar', 'Carlos', 
         'Atilio', 'Juan', 'Aristipio', 'Jorge', 'Abaracuatira', 'Emiliano', 'Angel',
         'David', 'Miguel', 'Daniel', 'Fernando', 'Alexander', 'Emmanuel', 'Alejandro', 'Maximiliano',
         'Jesus', 'Gael', 'Pedro', 'Manuel', 'Oscar', 'Miguel', 'John', 'Jaime', 'Francisco', 'Rafael',
         'Julio', 'Esteban', 'Mateo', 'Simon', 'Nicolas', 'Santiago', 'Sofia', 'Azucena', 'Maria', 'Valentina',
         'Amalia', 'Ximena', 'Martina', 'Regina', 'Britany', 'Mariana', 'Daniela', 'Natalia', 'Valeria', 'Isabella',
         'Camila', 'Manuela', 'Renata', 'Juliana', 'Victoria', 'Alejandra', 'Romina', 'Gabriela', 'Fernanda', 'Sara',
         'Andrea', 'Paula', 'Alexa', 'Laura', 'Guadalupe', 'Samantha', 'Paola', 'Melissa', 'Angie', 'Elizabeth', 'Vanessa',
         'Yamileth', 'Isabel', 'Fátima', 'Ana', 'Aitana', 'Luisa', 'Abigail', 'Paulina']

lnames = ['Garcia', 'Rodriguez', 'Gonzalez', 'Fernandez', 'Lopez', 'Martinez', 'Sanchez', 'Perez', 'Gomez',
          'Martin', 'Jimenez', 'Hernandez', 'Ruiz', 'Diaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero', 'Gutierrez',
          'Alonso', 'Navarro', 'Torres', 'Dominguez', 'Ramos', 'Vazquez', 'Ramirez', 'Gil', 'Serrano', 'Morales',
          'Molina', 'Blanco', 'Suarez', 'Castro', 'Ortega', 'Delgado', 'Ortiz', 'Marin', 'Rubio', 'Nuñez', 'Medina',
          'Sanz', 'Castillo', 'Iglesias', 'Cortes', 'Garrido', 'Santos', 'Guerrero', 'Lozano', 'Cano', 'Cruz', 'Mendez',
          'Flores', 'Prieto', 'Herrera', 'Peña', 'Leon', 'Marquez', 'Cabrera', 'Gallego', 'Calvo', 'Vidal', 'Campos',
          'Reyes', 'Vega', 'Fuentes', 'Carrasco', 'Diez', 'Aguilar', 'Caballero', 'Nieto', 'Santana', 'Vargas', 'Pascual',
          'Gimenez', 'Herrero', 'Hidalgo', 'Montero', 'Lorenzo', 'Santiago', 'Benitez', 'Duran', 'Ibañez', 'Arias',
          'Mora', 'Ferrer', 'Carmona', 'Vicente', 'Rojas', 'Soto', 'Crespo', 'Roman', 'Pastor', 'Velasco', 'Parra', 'Saez',
          'Moya', 'Bravo', 'Rivera', 'Gallardo', 'Soler']
    
def createTeacher(name, lname, phone, email, ci):
    t = Teacher()
    t.name = name
    t.lname = lname
    t.phone = phone
    t.email = email
    t.ci = ci
    t.save()
    user = User()
    user.access_token = token_urlsafe()
    user.login = t.email
    user.password = t.ci
    user.role = 'T'
    user.teacher = t
    user.save()
    
def createStudent(name, lname, phone, email, ci, rude):
    t = Student()
    t.name = name
    t.lname = lname
    t.phone = phone
    t.email = email
    t.ci = ci
    t.rude = rude
    t.save()
    user = User()
    user.access_token = token_urlsafe()
    user.login = t.email
    user.password = t.ci
    user.role = 'S'
    user.student = t
    user.save()
    return t

def genStudents():
    for i in range(1080):
        n = random.choice(names)
        ln = random.choice(lnames)
        r = random.randint(100, 999)
        e = n.lower() + '.' + ln.lower() + str(r) + '@gmail.com'
        ci = random.randint(1000000, 9999999)
        p = random.randint(1000000, 9999999)
        rude = random.randint(1000000, 9999999)
        t = createStudent(n, ln, p, e, ci, rude)
        c = Class.objects.get(pk=(253+(i%36)))
        c.students.add(t)
        c.save()
        
def genTeachers():
    for i in range(36):
        n = random.choice(names)
        ln = random.choice(lnames)
        r = random.randint(100, 999)
        e = n.lower() + '.' + ln.lower() + str(r) + '@gmail.com'
        ci = random.randint(1000000, 9999999)
        p = random.randint(1000000, 9999999)
        createTeacher(n, ln, p, e, ci)
        
t1dates = ['2024-12-04', '2024-12-11', '2024-12-18', '2024-12-25', '2025-01-01', '2025-01-08', '2025-01-15', '2025-01-22', '2025-01-29', '2025-02-05', '2025-02-12', '2025-02-19']
t2dates = ['2025-02-26', '2025-03-05', '2025-03-12', '2025-03-19', '2025-03-26', '2025-04-02', '2025-04-09', '2025-04-16', '2025-04-23', '2025-04-30', '2025-05-07', '2025-05-14']
t3dates = ['2025-05-21', '2025-05-29']

def genScores(st, students):
    for student in students:
        sc = Score()
        sc.score = random.randint(60, 100)
        sc.student = Student.objects.get(pk=student['id'])
        sc.target = st
        sc.save()
    
        
def genScoreTargets():
    c = Class.objects.get(stage='P', grade=1, parallel='A')
    s = c.subjects
    st = c.students
    ss = SubjectSerializerSimple(data=s, many=True)
    sts = StudentSerializer(data=st, many=True)
    ss.is_valid()
    sts.is_valid()
    subjects = ss.data
    students = sts.data
    for subject in subjects:
        cnt = 1
        for date in t1dates:
            st = ScoreTarget()
            st.subject = Subject.objects.get(pk=subject['id'])
            st._class = c
            st.title = 'S' + str(cnt)
            cnt += 1
            st.date = date
            st.trimester = 1
            st.save()
            genScores(st, students)
        for date in t2dates:
            st = ScoreTarget()
            st.subject = Subject.objects.get(pk=subject['id'])
            st._class = c
            st.title = 'S' + str(cnt)
            cnt += 1
            st.date = date
            st.trimester = 2
            st.save()
            genScores(st, students)
        for date in t3dates:
            st = ScoreTarget()
            st.subject = Subject.objects.get(pk=subject['id'])
            st._class = c
            st.title = 'S' + str(cnt)
            cnt += 1
            st.date = date
            st.trimester = 3
            st.save()
            genScores(st, students)
                

class automation(APIView):
    def get(self, request, format=None): 
        #genScoreTargets()
        return Response(status=200)
import datetime
from django.db import models
from django.utils.timezone import now

# Create your models here.

class Student(models.Model):
    name = models.TextField("Nombre(s)", max_length=100)
    lname = models.TextField("Apellido(s)", max_length=100)
    ci = models.BigIntegerField("Cédula de Identidad")
    phone = models.BigIntegerField("Teléfono", null=True)
    email = models.TextField("Correo electrónico", null=True)
    rude = models.BigIntegerField("Codigo RUDE")
    
    def __str__(self):
        return self.name + " " + self.lname
    
class Teacher(models.Model):
    name = models.TextField("Nombre(s)", max_length=100)
    lname = models.TextField("Apellido(s)", max_length=100)
    phone = models.BigIntegerField("Teléfono", null=True)
    email = models.TextField("Correo electrónico", null=True)
    ci = models.BigIntegerField("Cédula de Identidad")
    
    def __str__(self):
        return self.name + " " + self.lname
    
class Subject(models.Model):
    title = models.TextField("Titulo")
    teacher = models.ForeignKey(Teacher, verbose_name="Docente", on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Class(models.Model):
    grade = models.IntegerField("Curso")
    parallel = models.CharField("Paralelo")
    stage = models.CharField("Etapa") # P: Primaria, S: Secundaria
    year = models.IntegerField("Año")
    homeroom_teacher = models.ForeignKey(Teacher, verbose_name="Docente", on_delete=models.CASCADE, null = True)
    subjects = models.ManyToManyField(Subject, related_name='classes', blank=True)
    students = models.ManyToManyField(Student, related_name='students', blank=True)
    def __str__(self):
        return self.stage + str(self.grade) + self.parallel + '|' + str(self.year)

class Score(models.Model):
    
    class Trimester(models.IntegerChoices):
        t1 = 1, "1"
        t2 = 2, "2"
        t3 = 3, "3"
    
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="Estudiante", on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, verbose_name="Clase", on_delete=models.CASCADE)
    score = models.IntegerField("Nota")
    trimester = models.IntegerField("Trimestre", choices=Trimester.choices)
    
    class Meta:
        unique_together = ('subject', 'student', '_class', 'trimester')
    
class Assistance(models.Model):
    
    class Status(models.TextChoices):
        present = "present", "Presente"
        late = "late", "Tarde"
        missed = "missed", "Falta"
        license = "license", "Licencia"
    
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="Estudiante", on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, verbose_name="Clase", on_delete=models.CASCADE)
    date = models.DateField("Fecha")
    status = models.TextField("Estado", choices=Status.choices)
    
    class Meta:
        unique_together = ('subject', 'student', '_class', 'date')   
         
class Participation(models.Model):
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="Estudiante", on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, verbose_name="Clase", on_delete=models.CASCADE)
    date = models.DateField("Fecha")
    description = models.TextField("Descripcion", default=now)
    score = models.IntegerField("Nota", default=100)
    
class User(models.Model):
    login = models.TextField("Login", max_length=100)
    password = models.TextField("Password", max_length=100)
    access_token = models.TextField("Access Token", max_length=100)
    role = models.CharField("Role") # O: Dueño, A: Admin, S: Estudiante, T: Docente
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True)
    
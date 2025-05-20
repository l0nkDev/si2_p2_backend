from django.db import models

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
    
class Class(models.Model):
    grade = models.IntegerField("Curso")
    parallel = models.CharField("Paralelo")
    stage = models.CharField("Etapa") # P: Primaria, S: Secundaria
    year = models.IntegerField("Año")
    homeroom_teacher = models.ForeignKey(Teacher, verbose_name="Docente", on_delete=models.CASCADE)
    
class Subject(models.Model):
    title = models.TextField("Titulo"),
    teacher = models.ForeignKey(Teacher, verbose_name="Docente", on_delete=models.CASCADE)
    
class Subject_Class_Assignment(models.Model):
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, verbose_name="Clase", on_delete=models.CASCADE)
    
class Score(models.Model):
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="Estudiante", on_delete=models.CASCADE)
    score = models.IntegerField("Nota")
    trimester = models.IntegerField("Trimestre")
    
class User(models.Model):
    login = models.TextField("Login", max_length=100)
    password = models.TextField("Password", max_length=100)
    access_token = models.TextField("Access Token", max_length=100)
    role = models.CharField("Role") # O: Dueño, A: Admin, S: Estudiante, T: Docente
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True)
    
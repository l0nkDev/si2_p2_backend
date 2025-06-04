from django.db import models
from server.backend.core.models import Class, Student, Subject

# Create your models here.
    
class ClassSession(models.Model):
    class Status(models.TextChoices):
        juststarted = 'S', 'Acaba de empezar'
        late = 'L', 'Llega tarde'
        ended = 'E', 'Terminó'
    _class = models.ForeignKey(Class, verbose_name="Clase", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    date = models.DateField('Fecha')
    status = models.TextField('Estado', choices=Status.choices)
    class Meta:
        unique_together = ('_class', 'subject', 'date')
    
class Assistance(models.Model):
    class Status(models.TextChoices):
        present = "present", "Presente"
        late = "late", "Tarde"
        missed = "missed", "Falta"
        license = "license", "Licencia"
    student = models.ForeignKey(Student, verbose_name="Estudiante", related_name='assistances', on_delete=models.CASCADE)
    session = models.ForeignKey(ClassSession, verbose_name="Clase", on_delete=models.CASCADE)
    status = models.TextField("Estado", choices=Status.choices)
    class Meta:
        unique_together = ('student', 'session')  
    
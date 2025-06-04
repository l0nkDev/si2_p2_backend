from django.db import models
from django.utils.timezone import now
from server.backend.core.models import Class, Student, Subject

class Participation(models.Model):
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name="Estudiante", on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, verbose_name="Clase", on_delete=models.CASCADE)
    date = models.DateField("Fecha")
    description = models.TextField("Descripcion", default=now)
    score = models.IntegerField("Nota", default=100)
    
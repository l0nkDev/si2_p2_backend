from django.db import models
from server.backend.core.models import Class, Student, Subject

class ScoreTarget(models.Model):
    class Trimester(models.IntegerChoices):
        t1 = 1, "1"
        t2 = 2, "2"
        t3 = 3, "3"
    subject = models.ForeignKey(Subject, verbose_name="Materia", on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, verbose_name="Clase", on_delete=models.CASCADE)
    title = models.TextField("Título")
    trimester = models.IntegerField("Trimestre", choices=Trimester.choices)
    date = models.DateField("Fecha")

class Score(models.Model):
    student = models.ForeignKey(Student, verbose_name="Estudiante", on_delete=models.CASCADE)
    target = models.ForeignKey(ScoreTarget, verbose_name="Tarea", on_delete=models.CASCADE)
    score = models.IntegerField("Nota")
    class Meta:
        unique_together = ('student', 'target')
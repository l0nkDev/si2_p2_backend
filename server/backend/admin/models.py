from django.db import models
from server.backend.core.models import User

class fcm(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    token = models.TextField("Token", max_length=256)
    class Meta:
        unique_together = ('user', 'token')
        
class Log(models.Model):
    user = models.TextField("Usuario")
    role = models.TextField("Rol")
    login = models.TextField("Login")
    action = models.TextField("Acción")
    ip = models.TextField("IP")
    time = models.DateTimeField("Fecha y hora")
    
class Report(models.Model):
    params = models.TextField("Parametros")
    title = models.TextField("Título")
    time = models.DateTimeField("Fecha y hora")
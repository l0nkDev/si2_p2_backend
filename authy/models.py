from django.db import models

# Create your models here.

class User(models.Model):
    id = models.BigIntegerField("Registro", primary_key=True)
    name = models.CharField("Nombre", max_length=100)
    lname = models.CharField("Apeliido", max_length=100)
    password = models.CharField("Contraseña", max_length=100)
    access_token = models.CharField("Token de acceso", max_length=255, unique=True)
    
    def __str__(self):
        return self.name + " " + self.lname
    
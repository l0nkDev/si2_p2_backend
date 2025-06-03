import random
from secrets import token_urlsafe
from requests import Response
from rest_framework.views import APIView

from server.backend.models import Teacher, User

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

class automation(APIView):
    def get(self, request, format=None): 
        for i in range(36):
            n = random.choice(names)
            ln = random.choice(lnames)
            r = random.randint(100, 999)
            e = n.lower() + '.' + ln.lower() + str(r) + '@gmail.com'
            ci = random.randint(1000000, 9999999)
            p = random.randint(1000000, 9999999)
            createTeacher(n, ln, p, e, ci)
        return Response(status=200)
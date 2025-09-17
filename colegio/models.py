from django.db import models

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Oficina(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='oficinas')
    
    def __str__(self):
        return self.codigo

class SalonClase(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.codigo

class Persona(models.Model):
    TIPO_CHOICES = [
        ('profesor', 'Profesor'),
        ('administrativo', 'Administrativo'),
    ]
    TIPO_PROFESOR_CHOICES = [
        ('planta', 'Planta'),
        ('contratista', 'Contratista'),
    ]
    
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    tipo_profesor = models.CharField(max_length=20, choices=TIPO_PROFESOR_CHOICES, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='empleados')
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE, related_name='empleados')
    
    def __str__(self):
        return self.nombre
from django.db import models

# Create your models here.

class clientes(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    cedula = models.CharField(max_length=13)
    telefono = models.CharField(max_length=10)
    marca = models.CharField(max_length=20)
    matricula = models.CharField(max_length=20)
    diaentrada = models.CharField(max_length=100)
    vahiculo = models.CharField(max_length=10)
    dias = models.CharField(max_length=10, null=True)
    deuda = models.CharField(max_length=10, null=True)
    vigencia = models.BooleanField()

    def __str__(self):

        return self.nombre
    

    
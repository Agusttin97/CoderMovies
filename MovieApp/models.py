from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    email = models.EmailField()
    

class Pelicula(models.Model):
    
    titulo = models.CharField(max_length=30)
    genero = models.CharField(max_length=20)
    estreno = models.DateField()
    sinopsis = models.TextField()
    duracion = models.IntegerField()
    portada = models.ImageField(upload_to="portadas") 
    
    def __str__(self):
        return self.titulo
    
class Reseña(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    reseña = models.TextField()
    
class Categoria(models.Model):
    
    nombre = models.CharField(max_length=30)
    pelicula = models.ManyToManyField(Pelicula)
    
class Avatar(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="avatares", blank=True, null=True)
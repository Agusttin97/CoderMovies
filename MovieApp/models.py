from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver




# Create your models here.

    
class Pelicula(models.Model):
    
    titulo = models.CharField(max_length=30)
    genero = models.CharField(max_length=20)
    estreno = models.DateField()
    sinopsis = models.TextField()
    duracion = models.IntegerField()
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)
    
    
    def __str__(self):
        return self.titulo
    
class Usuario(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=True)
    apellido = models.CharField(max_length=30, null=True)
    email = models.EmailField(null=True)
    favoritos = models.ManyToManyField(Pelicula)
    
    def __str__(self):
        return self.user.username
    
@receiver(pre_delete, sender=Usuario)
def eliminar_relaciones_usuario(sender, instance, **kwargs):
    # Elimina las relaciones con películas antes de eliminar el usuario
    instance.favoritos.clear()
    
class Reseña(models.Model):
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    reseña = models.TextField()
    
    def __str__(self):
        return self.usuario - self.pelicula
  
class Avatar(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar', null=True)
    imagen = models.ImageField(upload_to="avatares", blank=True, null=True)
    
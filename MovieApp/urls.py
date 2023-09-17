from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', home, name='Home'),
    # LOGIN/LOGOUT - REGISTRO
    path('accounts/login', loginUser, name='Login'),
    path('accounts/singup', registro, name='Registro'),
    path('logout', LogoutView.as_view(template_name="logout.html"), name='Logout'),
    
    # CRUD PELICULAS
    path('lista-pelicula', PeliculaList.as_view(), name='ListaPelicula'),
    path('detalle-pelicula/<pk>/', PeliculaDetail.as_view(), name='DetallePelicula'),
    path('crea-pelicula', PeliculaCreate.as_view(), name='CreaPelicula'),
    path('actualiza-pelicula/<pk>', PeliculaUpdate.as_view(), name='ActualizaPelicula'),
    path('elimina-pelicula/<pk>', PeliculaDelete.as_view(), name='EliminaPelicula'),
    
    #Perfil
    path('accounts/profile', editarPerfil, name='Perfil'),
    
    # Reseñas
    path('actualiza-reseña/<pk>/', ReseñaUpdate.as_view(), name='ActualizaReseña'),
    path('elimina-reseña/<pk>/', ReseñaDelete.as_view(), name='EliminaReseña'),
    
    # Favoritos
    path('agrega-favoritos/<int:pelicula_id>/', agregaFavoritos, name='AgregaFavoritos'),
    path('elimina-favoritos/<int:pelicula_id>/', eliminaFavoritos, name='EliminaFavoritos'),
    path('lista-favoritos/', listaFavoritos, name='ListaFavoritos'),
    
    path('busca-pelicula/', buscaPelicula, name='BuscaPelicula'),
]
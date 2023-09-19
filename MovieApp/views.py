from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import UpdateView, DeleteView, FormMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page # Paginar


from .models import *
from .forms import *

# Create your views here.

def home(req):
    return render(req,'home.html')

#Login/Registro

def registro(req):
    if req.method == 'POST':
        miFormulario = UserCreationForm(req.POST)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            usuario = data["username"]
            miFormulario.save()
            
            # Crea un objeto Usuario relacionado con el nuevo usuario
            nuevo_usuario = User.objects.get(username=usuario)
            nuevo_objeto_usuario = Usuario.objects.create(user=nuevo_usuario, nombre='', apellido='', email='')
            
            return render(req, "home.html", {"mensaje": f"Usuario {usuario} creado con éxito!"})
        else:
            return render(req, "home.html", {"mensaje": "Formulario inválido"})
    else:
        miFormulario = UserCreationForm()
        return render(req, "registro.html", {"miFormulario": miFormulario})

def loginUser(req):
    
    
    if req.method == 'POST':
        
        miFormulario = AuthenticationForm(req, data=req.POST) #AuthenticationForm es un formulario vacio que crea django
        
        if miFormulario.is_valid():
            
            data = miFormulario.cleaned_data
            usuario = data["username"] 
            psw = data["password"]
            
            user = authenticate(username=usuario, password=psw) #Devuelve none o algo
            
            if user: #Si encuentra al usuario y su contraseña entra y loguea
                login(req, user)
                return render(req, "home.html", {"mensaje": f"Bienvenido {usuario}"})
            else:
                return render(req, "home.html", {"mensaje": "Datos incorrectos"})
        else:
             return render(req, "home.html", {"mensaje": "Formulario invalido"})       
    
    else:
        
        miFormulario = AuthenticationForm()
        return render(req, "login.html", {"miFormulario": miFormulario})
    

# Formularios
 
def peliculaForm(req: HttpRequest):
    
    if req.method == 'POST':
        
        miFormulario = PeliculaForm(req.POST) #Aca me llega toda la informacion del html
        
        if miFormulario.is_valid(): #Hace todas las validaciones y si paso entra
            
            data = miFormulario.cleaned_data
            
            pelicula = Pelicula(
                titulo=data["titulo"], 
                genero=data["genero"], 
                estreno=data["estreno"], 
                sinopsis=data["sinopsis"], 
                duracion=data["duracion"],
                )
            pelicula.save()
            return render(req, "home.html", {"mensaje": "Pelicula creada con exito"})
         
        else:
            return render(req, "home.html", {"mensaje": "Formulario invalido"})
    else: 
        
        miFormulario = PeliculaForm()
               
        return render(req, "crea_pelicula.html", {"miFormulario": miFormulario})


# CRUD Peliculas

class PeliculaList(ListView):
    model = Pelicula
    template_name = "lista_pelicula.html"
    context_object_name = "peliculas"
    paginate_by = 3 # Numero de peliculas por pagina
    
    def get_queryset(self):
        return Pelicula.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = Paginator(self.object_list, self.paginate_by)
        context["peliculas"] = paginator.get_page(page)
        return context  
    
class PeliculaDetail(FormMixin, DetailView):
    model = Pelicula
    template_name = "detalle_pelicula.html"
    context_object_name = "pelicula"
    form_class = ReseñaForm

    def get_success_url(self):
        return self.request.path  # Volver a la misma página después de enviar una reseña

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['reseñas'] = Reseña.objects.filter(pelicula=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.usuario = self.request.user
            form.instance.pelicula = self.object
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@method_decorator(staff_member_required, name='dispatch')
class PeliculaCreate(CreateView):
    model = Pelicula
    template_name = "crea_pelicula.html"
    form_class = PeliculaForm

    def form_valid(self, form):
        messages.success(self.request, "Pelicula creada con éxito")
        return super().form_valid(form)

    def get_success_url(self):
        return '/movie-app/'

@method_decorator(staff_member_required, name='dispatch')
class PeliculaUpdate(UpdateView):
    model = Pelicula
    template_name = "actualiza_pelicula.html"
    form_class = PeliculaForm

    def form_valid(self, form):
        messages.success(self.request, "Pelicula actualizada con éxito")
        return super().form_valid(form)

    def get_success_url(self):
        return '/movie-app/'

@method_decorator(staff_member_required, name='dispatch') 
class PeliculaDelete(DeleteView):
    model = Pelicula 
    template_name = "elimina_pelicula.html"
    success_url = "/movie-app/lista-pelicula"


# Perfil
@login_required
def editarPerfil(req):
    usuario = req.user
    try:
        avatar = usuario.avatar
    except Avatar.DoesNotExist:
        avatar = None
    
    if req.method == 'POST':
        
        miFormulario = UserEditForm(req.POST, instance=usuario)
        formulario_avatar = AvatarForm(req.POST, req.FILES, instance=avatar)
        
        if miFormulario.is_valid() and formulario_avatar.is_valid():
            data = miFormulario.cleaned_data
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]
            usuario.email = data["email"]
            if data["password1"]:
                usuario.set_password(data["password1"])
            usuario.save()
            
            if avatar is None:
                avatar = Avatar(user=usuario)
            data_avatar = formulario_avatar.cleaned_data
            avatar.imagen = data_avatar["imagen"]
            avatar.save()
            
            
            return render(req, "editar_perfil.html", {"mensaje": "Perfil actualizado con exito" ,"miFormularioUsuario": miFormulario, "miFormularioAvatar": formulario_avatar})
    else:
        miFormulario = UserEditForm(instance=usuario)
        formulario_avatar = AvatarForm(instance=avatar)
        
        return render(req, "editar_perfil.html", {"miFormularioUsuario": miFormulario, "miFormularioAvatar": formulario_avatar})
    

# CRUD Reseñas 
class ReseñaCreate(LoginRequiredMixin, CreateView):
    model = Reseña
    form_class = ReseñaForm  # Ajusta el nombre del formulario según tu aplicación
    template_name = "detalle_pelicula.html"  # Asegúrate de que la plantilla sea la correcta
    context_object_name = "pelicula"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.pelicula = self.pelicula  # Asigna la película relacionada
        form.save()
        return redirect('detalle-pelicula', pk=self.pelicula.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReseñaForm()  # Ajusta el nombre del formulario según tu aplicación
        return context
    
class ReseñaUpdate(LoginRequiredMixin, UpdateView):
    model = Reseña
    fields = ['reseña']
    template_name = 'actualiza_reseña.html'

    def get_success_url(self):
        return reverse_lazy('DetallePelicula', kwargs={'pk': self.object.pelicula.pk})

    def get_object(self, queryset=None):
        # Obtener la reseña por ID y verificar si el usuario actual es el autor
        obj = get_object_or_404(Reseña, pk=self.kwargs['pk'], usuario=self.request.user)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pelicula'] = self.object.pelicula  # Agregar la película al contexto
        return context
    
class ReseñaDelete(LoginRequiredMixin, DeleteView):
    model = Reseña
    template_name = 'elimina_reseña.html'

    def get_success_url(self):
        return reverse_lazy('DetallePelicula', kwargs={'pk': self.object.pelicula.pk})

    def get_object(self, queryset=None):
        # Obtener la reseña por ID y verificar si el usuario actual es el autor
        obj = get_object_or_404(Reseña, pk=self.kwargs['pk'], usuario=self.request.user)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pelicula'] = self.object.pelicula  # Agregar la película al contexto
        return context
    
    
# Lista de peliculas favoritas

@login_required
def agregaFavoritos(req, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    usuario = req.user.usuario  # Acceder al perfil del usuario

    if pelicula not in usuario.favoritos.all():
        usuario.favoritos.add(pelicula)
        return render(req, 'home.html', {'mensaje': 'Pelicula agregada con exito.' })


    return redirect('ListaPelicula')

@login_required
def eliminaFavoritos(req, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)
    usuario = req.user.usuario

    if pelicula in usuario.favoritos.all():
        usuario.favoritos.remove(pelicula)
        return render(req, 'home.html', {'mensaje': 'Pelicula eliminada con exito.' })

    return redirect('ListaPelicula')

@login_required
def listaFavoritos(req):

    usuario = req.user.usuario
    peliculas_favoritas = usuario.favoritos.all()

    return render(req, 'lista_favoritos.html', {'peliculas_favoritas': peliculas_favoritas})


def buscaPelicula(req):
    if req.method == 'POST':
        nombre_pelicula = req.POST.get('nombre_pelicula', '')
        if nombre_pelicula:
            try:
                pelicula = Pelicula.objects.get(titulo__icontains=nombre_pelicula)
                return redirect('DetallePelicula', pk=pelicula.id)
            except Pelicula.DoesNotExist:
                error_message = "No se encontro la pelicula"
                return render(req, 'lista_pelicula.html', {'error_message': error_message})
    return render(req, 'lista_pelicula.html')


def sobreMi(req):
    return render(req, 'sobre_mi.html')





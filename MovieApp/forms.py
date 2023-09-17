from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import *


class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ('__all__')

        widgets = {
            'estreno': forms.DateInput(attrs={'type': 'date'}),
        }
        
class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['reseña']
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'email')
        
class UserEditForm(UserChangeForm): #Hereda de UserChangeForm
    
    password = forms.CharField( #Elimina el mensaje de ayuda del password
        help_text = "",
        widget = forms.HiddenInput(), required = False 
    )
    
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=False) #Con un widget modificamos el comportamiento de los campos
    password2 = forms.CharField(label="Repita contraseña", widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2') #Muestra solo estos campos
        
    def clean_password2(self):
        
        print(self.cleaned_data)
        
        password2 = self.cleaned_data["password2"] #El primer password2 es una variable creada dentro del metodo, y el segundo password2(entre corchetes) se refiere a la password que ingreso el usuario en el form arriba
        if password2 != self.cleaned_data["password1"]:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2
    
class AvatarForm(forms.ModelForm):
    
    class Meta:
        model = Avatar
        fields = ('imagen',)
        

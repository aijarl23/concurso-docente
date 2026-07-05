from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label='Nombres')
    last_name = forms.CharField(max_length=150, required=True, label='Apellidos')
    email = forms.EmailField(required=True)
    area_concurso = forms.ChoiceField(choices=Usuario.AREA_CHOICES, label='Área del concurso')
    entidad_territorial = forms.CharField(max_length=100, required=False, label='Entidad territorial')
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 
                  'area_concurso', 'entidad_territorial', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.area_concurso = self.cleaned_data['area_concurso']
        user.entidad_territorial = self.cleaned_data.get('entidad_territorial', '')
        if commit:
            user.save()
        return user

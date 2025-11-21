from django.contrib import admin
from .models import Pacientes, HistorialesClinicos, ContactosEmergencia, Usuarios, Roles


@admin.register(Pacientes)
class PacientesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'apellidos', 'celular', 'ultima_consulta')
    search_fields = ('nombres', 'apellidos', 'celular')


@admin.register(HistorialesClinicos)
class HistorialesClinicosAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'creado_en')
    search_fields = ('paciente__nombres', 'paciente__apellidos')


@admin.register(ContactosEmergencia)
class ContactosEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'paciente')
    search_fields = ('nombre', 'telefono')


@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'activo', 'creado_en')
    search_fields = ('username', 'email')


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
from django.contrib import admin

# Register your models here.

# This is an auto-generated Django model module.

# You'll have to do the following manually to clean this up:

#   * Rearrange models' order

#   * Make sure each model has one field with primary_key=True

#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior

#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table

# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models





class Antecedentes(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    historial = models.ForeignKey('HistorialesClinicos', on_delete=models.DO_NOTHING, db_column='historial_id')

    tipo = models.CharField(max_length=20)  # 'familiar', 'ginecologico', 'no_patologico', 'patologico'

    observaciones = models.TextField(blank=True, null=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            paciente_nombre = f"{self.historial.paciente.nombres} {self.historial.paciente.apellidos}"
            return f"Antecedente {self.tipo} - {paciente_nombre}"
        except:
            return f"Antecedente {self.tipo} - {self.id}"

    class Meta:

        managed = True

        db_table = 'antecedentes'





class AntecedentesFamiliares(models.Model):

    antecedente = models.OneToOneField(Antecedentes, on_delete=models.CASCADE, primary_key=True, db_column='antecedente_id')

    alergia = models.BooleanField(default=False)

    asma_bronquial = models.BooleanField(default=False)

    cardiologicos = models.BooleanField(default=False)

    oncologicos = models.BooleanField(default=False)

    discrasias_sanguineas = models.BooleanField(default=False)

    diabetes = models.BooleanField(default=False)

    hipertension_arterial = models.BooleanField(default=False)

    renales = models.BooleanField(default=False)



    class Meta:

        managed = True

        db_table = 'antecedentes_familiares'





class AntecedentesGinecologicos(models.Model):

    antecedente = models.OneToOneField(Antecedentes, on_delete=models.CASCADE, primary_key=True, db_column='antecedente_id')

    embarazada = models.BooleanField(default=False)

    meses_embarazo = models.IntegerField(blank=True, null=True)

    anticonceptivos = models.BooleanField(default=False)



    class Meta:

        managed = True

        db_table = 'antecedentes_ginecologicos'





class AntecedentesNoPatologicos(models.Model):

    antecedente = models.OneToOneField(Antecedentes, on_delete=models.CASCADE, primary_key=True, db_column='antecedente_id')

    respira_boca = models.BooleanField(default=False)

    alimentos_citricos = models.BooleanField(default=False)

    muerde_unas = models.BooleanField(default=False)

    muerde_objetos = models.BooleanField(default=False)

    fuma = models.BooleanField(default=False)

    cantidad_cigarros = models.IntegerField(blank=True, null=True)

    apretamiento_dentario = models.BooleanField(default=False)



    class Meta:

        managed = True

        db_table = 'antecedentes_no_patologicos'





class AntecedentesPatologicosPersonales(models.Model):

    antecedente = models.OneToOneField(Antecedentes, on_delete=models.CASCADE, primary_key=True, db_column='antecedente_id')

    # Estado de salud
    ESTADO_CHOICES = [
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala')
    ]
    estado_salud = models.CharField(max_length=10, choices=ESTADO_CHOICES, blank=True, null=True)

    fecha_ultimo_examen = models.DateField(blank=True, null=True)

    bajo_tratamiento_medico = models.BooleanField(default=False)

    toma_medicamentos = models.BooleanField(default=False)

    intervencion_quirurgica = models.BooleanField(default=False)

    sangra_excesivamente = models.BooleanField(default=False)

    problema_sanguineo = models.BooleanField(default=False)

    anemia = models.BooleanField(default=False)

    problemas_oncologicos = models.BooleanField(default=False)

    leucemia = models.BooleanField(default=False)

    problemas_renales = models.BooleanField(default=False)

    hemofilia = models.BooleanField(default=False)

    transfusion_sanguinea = models.BooleanField(default=False)

    deficit_vitamina_k = models.BooleanField(default=False)

    consume_drogas = models.BooleanField(default=False)

    problemas_corazon = models.BooleanField(default=False)

    # Alergias
    alergia_penicilina = models.BooleanField(default=False)

    alergia_anestesia = models.BooleanField(default=False)

    alergia_aspirina = models.BooleanField(default=False)

    alergia_yodo = models.BooleanField(default=False)

    alergia_otros = models.TextField(blank=True, null=True)

    fiebre_reumatica = models.BooleanField(default=False)

    asma = models.BooleanField(default=False)

    diabetes = models.BooleanField(default=False)

    ulcera_gastrica = models.BooleanField(default=False)

    # Tensión arterial
    TENSION_CHOICES = [
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('baja', 'Baja')
    ]
    tension_arterial = models.CharField(max_length=10, choices=TENSION_CHOICES, blank=True, null=True)

    herpes_aftas_recurrentes = models.BooleanField(default=False)

    enfermedades_venereas = models.BooleanField(default=False)

    vih_positivo = models.BooleanField(default=False)

    otros = models.TextField(blank=True, null=True)



    class Meta:

        managed = True

        db_table = 'antecedentes_patologicos_personales'





class AuthGroup(models.Model):

    name = models.CharField(unique=True, max_length=150)



    class Meta:

        managed = False

        db_table = 'auth_group'





class AuthGroupPermissions(models.Model):

    id = models.BigAutoField(primary_key=True)

    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'auth_group_permissions'

        unique_together = (('group', 'permission'),)





class AuthPermission(models.Model):

    name = models.CharField(max_length=255)

    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)

    codename = models.CharField(max_length=100)



    class Meta:

        managed = False

        db_table = 'auth_permission'

        unique_together = (('content_type', 'codename'),)





class AuthUser(models.Model):

    password = models.CharField(max_length=128)

    last_login = models.DateTimeField(blank=True, null=True)

    is_superuser = models.IntegerField()

    username = models.CharField(unique=True, max_length=150)

    first_name = models.CharField(max_length=150)

    last_name = models.CharField(max_length=150)

    email = models.CharField(max_length=254)

    is_staff = models.IntegerField()

    is_active = models.IntegerField()

    date_joined = models.DateTimeField()



    class Meta:

        managed = False

        db_table = 'auth_user'





class AuthUserGroups(models.Model):

    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'auth_user_groups'

        unique_together = (('user', 'group'),)





class AuthUserUserPermissions(models.Model):

    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'auth_user_user_permissions'

        unique_together = (('user', 'permission'),)





class ContactosEmergencia(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, blank=True, null=True)

    nombre = models.CharField(max_length=100)

    parentesco = models.CharField(max_length=50, blank=True, null=True)

    telefono = models.CharField(max_length=20, blank=True, null=True)



    class Meta:

        managed = False

        db_table = 'contactos_emergencia'





class DjangoAdminLog(models.Model):

    action_time = models.DateTimeField()

    object_id = models.TextField(blank=True, null=True)

    object_repr = models.CharField(max_length=200)

    action_flag = models.PositiveSmallIntegerField()

    change_message = models.TextField()

    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)

    user = models.ForeignKey(AuthUser, models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'django_admin_log'





class DjangoContentType(models.Model):

    app_label = models.CharField(max_length=100)

    model = models.CharField(max_length=100)



    class Meta:

        managed = False

        db_table = 'django_content_type'

        unique_together = (('app_label', 'model'),)





class DjangoMigrations(models.Model):

    id = models.BigAutoField(primary_key=True)

    app = models.CharField(max_length=255)

    name = models.CharField(max_length=255)

    applied = models.DateTimeField()



    class Meta:

        managed = False

        db_table = 'django_migrations'





class DjangoSession(models.Model):

    session_key = models.CharField(primary_key=True, max_length=40)

    session_data = models.TextField()

    expire_date = models.DateTimeField()



    class Meta:

        managed = False

        db_table = 'django_session'





class HistorialesClinicos(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    paciente = models.ForeignKey('Pacientes', on_delete=models.CASCADE)

    creado_en = models.DateTimeField(auto_now_add=True)



    class Meta:

        managed = True

        db_table = 'historiales_clinicos'





class ModeloPermisos(models.Model):

    pk = models.CompositePrimaryKey('modelo_id', 'permiso_id')

    modelo = models.ForeignKey('Modelos', models.DO_NOTHING)

    permiso = models.ForeignKey('Permisos', models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'modelo_permisos'





class ModeloRoles(models.Model):

    pk = models.CompositePrimaryKey('modelo_id', 'rol_id')

    modelo = models.ForeignKey('Modelos', models.DO_NOTHING)

    rol = models.ForeignKey('Roles', models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'modelo_roles'





class Modelos(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    nombre = models.CharField(unique=True, max_length=50)

    descripcion = models.TextField(blank=True, null=True)



    class Meta:

        managed = False

        db_table = 'modelos'





class Pacientes(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    apellidos = models.CharField(max_length=100)

    nombres = models.CharField(max_length=100)

    edad = models.IntegerField(blank=True, null=True)

    sexo = models.CharField(max_length=10, blank=True, null=True)

    fecha_nacimiento = models.DateField(blank=True, null=True)

    estado_civil = models.CharField(max_length=20, blank=True, null=True)

    ocupacion = models.CharField(max_length=100, blank=True, null=True)

    direccion = models.TextField(blank=True, null=True)

    celular = models.CharField(max_length=20, blank=True, null=True)

    ultima_consulta = models.DateField(blank=True, null=True)

    motivo_ultima_consulta = models.TextField(blank=True, null=True)

    creado_en = models.DateTimeField(auto_now_add=True)



    class Meta:

        managed = True

        db_table = 'pacientes'





class Permisos(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    nombre = models.CharField(unique=True, max_length=100)

    descripcion = models.TextField(blank=True, null=True)



    class Meta:

        managed = False

        db_table = 'permisos'





class RolPermisos(models.Model):

    pk = models.CompositePrimaryKey('rol_id', 'permiso_id')

    rol = models.ForeignKey('Roles', models.DO_NOTHING)

    permiso = models.ForeignKey(Permisos, models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'rol_permisos'





class Roles(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    nombre = models.CharField(unique=True, max_length=50)

    descripcion = models.TextField(blank=True, null=True)



    class Meta:

        managed = False

        db_table = 'roles'





class UsuarioRoles(models.Model):

    pk = models.CompositePrimaryKey('usuario_id', 'rol_id')

    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)

    rol = models.ForeignKey(Roles, models.DO_NOTHING)



    class Meta:

        managed = False

        db_table = 'usuario_roles'





class Usuarios(models.Model):

    id = models.CharField(primary_key=True, max_length=36)

    username = models.CharField(unique=True, max_length=50)

    email = models.CharField(unique=True, max_length=100)

    password_hash = models.TextField()

    activo = models.IntegerField(blank=True, null=True)

    creado_en = models.DateTimeField()



    class Meta:

        managed = False

        db_table = 'usuarios'


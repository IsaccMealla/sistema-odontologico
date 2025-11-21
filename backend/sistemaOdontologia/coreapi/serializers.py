from rest_framework import serializers
from django.utils import timezone
import uuid
from .models import Pacientes, HistorialesClinicos, ContactosEmergencia, Usuarios, Roles
from .models import (
    Antecedentes,
    AntecedentesFamiliares,
    AntecedentesGinecologicos,
    AntecedentesNoPatologicos,
    AntecedentesPatologicosPersonales,
)


class PacienteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    creado_en = serializers.DateTimeField(required=False)

    class Meta:
        model = Pacientes
        fields = '__all__'

    def create(self, validated_data):
        # Ensure id and creado_en are set for legacy DB
        if not validated_data.get('id'):
            validated_data['id'] = str(uuid.uuid4())
        if not validated_data.get('creado_en'):
            validated_data['creado_en'] = timezone.now()
        
        # Create the patient (no automatic historial creation)
        paciente = super().create(validated_data)
        return paciente


class HistorialClinicoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    creado_en = serializers.DateTimeField(required=False)

    class Meta:
        model = HistorialesClinicos
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('id'):
            validated_data['id'] = str(uuid.uuid4())
        if not validated_data.get('creado_en'):
            validated_data['creado_en'] = timezone.now()
        return super().create(validated_data)


class AntecedenteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    creado_en = serializers.DateTimeField(required=False)
    paciente_nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Antecedentes
        fields = ['id', 'historial', 'tipo', 'observaciones', 'creado_en', 'paciente_nombre_completo']

    def get_paciente_nombre_completo(self, obj):
        try:
            return f"{obj.historial.paciente.nombres} {obj.historial.paciente.apellidos}"
        except:
            return "Paciente Desconocido"

    def create(self, validated_data):
        if not validated_data.get('id'):
            validated_data['id'] = str(uuid.uuid4())
        if not validated_data.get('creado_en'):
            validated_data['creado_en'] = timezone.now()
        return super().create(validated_data)


class ContactoEmergenciaSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        model = ContactosEmergencia
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('id'):
            validated_data['id'] = str(uuid.uuid4())
        return super().create(validated_data)


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    id = serializers.CharField(required=False)
    creado_en = serializers.DateTimeField(required=False)

    class Meta:
        model = Usuarios
        # do not expose password_hash for write here; handle separately
        exclude = ('password_hash',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not validated_data.get('id'):
            validated_data['id'] = str(uuid.uuid4())
        if not validated_data.get('creado_en'):
            validated_data['creado_en'] = timezone.now()
        if password is not None:
            # store a sha256 hash in password_hash field
            import hashlib
            validated_data['password_hash'] = hashlib.sha256(password.encode()).hexdigest()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # handle password update
        password = validated_data.pop('password', None)
        if password is not None:
            import hashlib
            instance.password_hash = hashlib.sha256(password.encode()).hexdigest()
        return super().update(instance, validated_data)


class RolSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        model = Roles
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('id'):
            validated_data['id'] = str(uuid.uuid4())
        return super().create(validated_data)


# Serializer base para Antecedentes
class AntecedenteBaseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    paciente_nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Antecedentes
        fields = '__all__'
    
    def get_paciente_nombre_completo(self, obj):
        try:
            paciente = obj.historial.paciente
            return f"{paciente.nombres} {paciente.apellidos}".strip()
        except:
            return ""
    
    def create(self, validated_data):
        if not validated_data.get('id'):
            validated_data['id'] = str(uuid.uuid4())
        return super().create(validated_data)


# Serializers para cada tipo de antecedente con estructura padre-hijo
class AntecedenteFamiliarSerializer(serializers.ModelSerializer):
    # Campos del antecedente base
    historial = serializers.CharField()
    observaciones = serializers.CharField(required=False, allow_blank=True)
    paciente_nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = AntecedentesFamiliares
        fields = '__all__'
    
    def get_paciente_nombre_completo(self, obj):
        try:
            paciente = obj.antecedente.historial.paciente
            return f"{paciente.nombres} {paciente.apellidos}".strip()
        except:
            return ""
    
    def create(self, validated_data):
        # Extraer datos del antecedente base
        historial_id = validated_data.pop('historial')
        observaciones = validated_data.pop('observaciones', '')
        
        # Crear el antecedente base
        antecedente_base = Antecedentes.objects.create(
            id=str(uuid.uuid4()),
            historial_id=historial_id,
            tipo='familiar',
            observaciones=observaciones
        )
        
        # Crear el antecedente específico
        validated_data['antecedente'] = antecedente_base
        return super().create(validated_data)


class AntecedenteGinecologicoSerializer(serializers.ModelSerializer):
    historial = serializers.CharField()
    observaciones = serializers.CharField(required=False, allow_blank=True)
    paciente_nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = AntecedentesGinecologicos
        fields = '__all__'
    
    def get_paciente_nombre_completo(self, obj):
        try:
            paciente = obj.antecedente.historial.paciente
            return f"{paciente.nombres} {paciente.apellidos}".strip()
        except:
            return ""
    
    def create(self, validated_data):
        historial_id = validated_data.pop('historial')
        observaciones = validated_data.pop('observaciones', '')
        
        antecedente_base = Antecedentes.objects.create(
            id=str(uuid.uuid4()),
            historial_id=historial_id,
            tipo='ginecologico',
            observaciones=observaciones
        )
        
        validated_data['antecedente'] = antecedente_base
        return super().create(validated_data)


class AntecedenteNoPatologicoSerializer(serializers.ModelSerializer):
    historial = serializers.CharField()
    observaciones = serializers.CharField(required=False, allow_blank=True)
    paciente_nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = AntecedentesNoPatologicos
        fields = '__all__'
    
    def get_paciente_nombre_completo(self, obj):
        try:
            paciente = obj.antecedente.historial.paciente
            return f"{paciente.nombres} {paciente.apellidos}".strip()
        except:
            return ""
    
    def create(self, validated_data):
        historial_id = validated_data.pop('historial')
        observaciones = validated_data.pop('observaciones', '')
        
        antecedente_base = Antecedentes.objects.create(
            id=str(uuid.uuid4()),
            historial_id=historial_id,
            tipo='no_patologico',
            observaciones=observaciones
        )
        
        validated_data['antecedente'] = antecedente_base
        return super().create(validated_data)


class AntecedentePatologicoSerializer(serializers.ModelSerializer):
    historial = serializers.CharField()
    observaciones = serializers.CharField(required=False, allow_blank=True)
    paciente_nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = AntecedentesPatologicosPersonales
        fields = '__all__'
    
    def get_paciente_nombre_completo(self, obj):
        try:
            paciente = obj.antecedente.historial.paciente
            return f"{paciente.nombres} {paciente.apellidos}".strip()
        except:
            return ""
    
    def create(self, validated_data):
        historial_id = validated_data.pop('historial')
        observaciones = validated_data.pop('observaciones', '')
        
        antecedente_base = Antecedentes.objects.create(
            id=str(uuid.uuid4()),
            historial_id=historial_id,
            tipo='patologico',
            observaciones=observaciones
        )
        
        validated_data['antecedente'] = antecedente_base
        return super().create(validated_data)


# Serializer para vista consolidada de antecedentes
class AntecedenteConsolidadoSerializer(serializers.ModelSerializer):
    paciente_nombre_completo = serializers.SerializerMethodField()
    paciente_id = serializers.SerializerMethodField()
    tipo_display = serializers.SerializerMethodField()
    detalles = serializers.SerializerMethodField()
    
    # Campos para escribir detalles específicos
    detalles_familiares = serializers.DictField(required=False, write_only=True)
    detalles_ginecologicos = serializers.DictField(required=False, write_only=True)
    detalles_no_patologicos = serializers.DictField(required=False, write_only=True)
    detalles_patologicos = serializers.DictField(required=False, write_only=True)
    
    class Meta:
        model = Antecedentes
        fields = ['id', 'historial', 'tipo', 'tipo_display', 'observaciones', 'creado_en', 
                 'paciente_nombre_completo', 'paciente_id', 'detalles', 
                 'detalles_familiares', 'detalles_ginecologicos', 
                 'detalles_no_patologicos', 'detalles_patologicos']
        extra_kwargs = {
            'id': {'required': False},
            'creado_en': {'read_only': True},
        }
    
    def to_representation(self, instance):
        # Obtener la representación base
        data = super().to_representation(instance)
        
        # Obtener detalles específicos
        detalles = self.get_detalles(instance)
        
        # Aplanar los detalles en el nivel superior
        data.update(detalles)
        
        return data
    
    def get_paciente_nombre_completo(self, obj):
        try:
            paciente = obj.historial.paciente
            return f"{paciente.nombres} {paciente.apellidos}".strip()
        except:
            return ""
    
    def get_paciente_id(self, obj):
        try:
            return obj.historial.paciente.id
        except:
            return None
    
    def get_tipo_display(self, obj):
        tipos = {
            'familiar': 'Antecedentes Familiares',
            'ginecologico': 'Antecedentes Ginecologicos', 
            'no_patologico': 'Antecedentes No Patologicos',
            'patologico': 'Antecedentes Patologicos Personales'
        }
        return tipos.get(obj.tipo, obj.tipo)
    
    def get_detalles(self, obj):
        # Obtener los detalles específicos según el tipo
        detalles = {}
        
        try:
            if obj.tipo == 'familiar':
                detalle = obj.antecedentesfamiliares
                # Usar reflexión para obtener todos los campos
                for field in detalle._meta.fields:
                    if field.name not in ['id', 'antecedente']:
                        detalles[field.name] = getattr(detalle, field.name, None)
                        
            elif obj.tipo == 'ginecologico':
                detalle = obj.antecedentesginecologicos
                for field in detalle._meta.fields:
                    if field.name not in ['id', 'antecedente']:
                        detalles[field.name] = getattr(detalle, field.name, None)
                        
            elif obj.tipo == 'no_patologico':
                detalle = obj.antecedentesnopatologicos
                for field in detalle._meta.fields:
                    if field.name not in ['id', 'antecedente']:
                        detalles[field.name] = getattr(detalle, field.name, None)
                        
            elif obj.tipo == 'patologico':
                detalle = obj.antecedentespatologicospersonales
                for field in detalle._meta.fields:
                    if field.name not in ['id', 'antecedente']:
                        detalles[field.name] = getattr(detalle, field.name, None)
                        
        except Exception as e:
            print(f"Error obteniendo detalles para {obj.tipo}: {e}")
            
        return detalles
    
    def create(self, validated_data):
        import uuid
        print(f"=== CREATE ANTECEDENTE ===")
        print(f"Datos recibidos: {validated_data}")
        
        # Generar UUID para el ID
        if 'id' not in validated_data:
            validated_data['id'] = str(uuid.uuid4())
        
        # Extraer campos base del antecedente
        historial = validated_data.get('historial')
        tipo = validated_data.get('tipo')
        observaciones = validated_data.get('observaciones', '')
        
        print(f"Historial: {historial}, Tipo: {tipo}")
        
        # Crear el antecedente base
        antecedente = Antecedentes.objects.create(
            id=validated_data['id'],
            historial_id=historial,
            tipo=tipo,
            observaciones=observaciones
        )
        
        # Extraer todos los campos específicos (excluyendo los campos base)
        campos_excluir = {'id', 'historial', 'tipo', 'observaciones', 'creado_en', 
                         'paciente_nombre_completo', 'paciente_id', 'tipo_display', 'detalles',
                         'detalles_familiares', 'detalles_ginecologicos', 
                         'detalles_no_patologicos', 'detalles_patologicos'}
        
        campos_especificos = {k: v for k, v in validated_data.items() if k not in campos_excluir}
        print(f"Campos específicos: {campos_especificos}")
        
        # Crear el detalle específico según el tipo
        try:
            if tipo == 'familiar':
                AntecedentesFamiliares.objects.create(
                    antecedente=antecedente,
                    **campos_especificos
                )
                print("Antecedente familiar creado")
            elif tipo == 'ginecologico':
                AntecedentesGinecologicos.objects.create(
                    antecedente=antecedente,
                    **campos_especificos
                )
                print("Antecedente ginecológico creado")
            elif tipo == 'no_patologico':
                AntecedentesNoPatologicos.objects.create(
                    antecedente=antecedente,
                    **campos_especificos
                )
                print("Antecedente no patológico creado")
            elif tipo == 'patologico':
                AntecedentesPatologicosPersonales.objects.create(
                    antecedente=antecedente,
                    **campos_especificos
                )
                print("Antecedente patológico creado")
            
            print(f"Antecedente {tipo} creado exitosamente con ID: {antecedente.id}")
        except Exception as e:
            print(f"Error creando detalle específico: {e}")
            # Si hay error, eliminar el antecedente base
            antecedente.delete()
            raise
        
        return antecedente

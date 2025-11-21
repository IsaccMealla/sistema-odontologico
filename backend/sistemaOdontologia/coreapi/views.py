from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
	Pacientes,
	HistorialesClinicos,
	ContactosEmergencia,
	Usuarios,
	Roles,
	Antecedentes,
	AntecedentesFamiliares,
	AntecedentesGinecologicos,
	AntecedentesNoPatologicos,
	AntecedentesPatologicosPersonales,
)
from .serializers import (
	PacienteSerializer,
	HistorialClinicoSerializer,
	ContactoEmergenciaSerializer,
	UsuarioSerializer,
	RolSerializer,
	AntecedenteSerializer,
	AntecedenteConsolidadoSerializer,
)


class PacienteViewSet(viewsets.ModelViewSet):
	queryset = Pacientes.objects.all()
	serializer_class = PacienteSerializer


class HistorialClinicoViewSet(viewsets.ModelViewSet):
	queryset = HistorialesClinicos.objects.all()
	serializer_class = HistorialClinicoSerializer


class ContactoEmergenciaViewSet(viewsets.ModelViewSet):
	queryset = ContactosEmergencia.objects.all()
	serializer_class = ContactoEmergenciaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
	queryset = Usuarios.objects.all()
	serializer_class = UsuarioSerializer


class RolViewSet(viewsets.ModelViewSet):
	queryset = Roles.objects.all()
	serializer_class = RolSerializer


class AntecedenteViewSet(viewsets.ModelViewSet):
	"""Vista para la tabla padre Antecedentes"""
	queryset = Antecedentes.objects.select_related('historial__paciente').all()
	serializer_class = AntecedenteSerializer


# Vista consolidada de antecedentes
class AntecedenteConsolidadoViewSet(viewsets.ModelViewSet):
	"""Vista consolidada de todos los antecedentes con nombres de pacientes"""
	queryset = Antecedentes.objects.select_related('historial__paciente').all()
	serializer_class = AntecedenteConsolidadoSerializer
	
	def list(self, request):
		try:
			antecedentes = self.queryset.all()
			serializer = self.serializer_class(antecedentes, many=True)
			return Response(serializer.data)
		except Exception as e:
			print(f"Error in AntecedenteConsolidadoViewSet.list: {e}")
			return Response({'error': str(e)}, status=500)
	
	def create(self, request):
		try:
			print(f"Received data for antecedente: {request.data}")
			serializer = self.serializer_class(data=request.data)
			if serializer.is_valid():
				antecedente = serializer.save()
				return Response(self.serializer_class(antecedente).data, status=201)
			else:
				print(f"Serializer errors: {serializer.errors}")
				return Response(serializer.errors, status=400)
		except Exception as e:
			print(f"Error creating antecedente: {e}")
			return Response({'error': str(e)}, status=500)

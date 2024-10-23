from rest_framework import serializers
from .models import Comedor, FuncionamientoComedor#, OtrasActividadesComedor


class ComedorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comedor
		read_only_fields = ['id', 'servicio_comedor', 'activo', 'organizacion_regional', 'provincia', 'departamento', 'gobierno_local', 'localidad', 'barrio', 'latitud', 'longitud', 'ubicacion_georreferencial', 'fecha_inicio_actividad', 'descripcion', 'actividades', 'cantidad_trabajadores', 'asistentes_diarios', 'tipos_energia', 'fuente_agua', 'fuente_agua_potable', 'responsable_comedor']
		fields = '__all__' #si quiero todos los campos

class FuncionamientoComedorSerializer(serializers.ModelSerializer):

    class Meta:
        model = FuncionamientoComedor
        fields = ['comedor', 'dia', 'funcionamiento'] #si quiero todos los campos

class FuncionamientoSerializer(serializers.Serializer):
	funcionamiento = serializers.CharField(max_length=50)

class FuncionamientoDiaSerializers(serializers.Serializer):
	dia = serializers.CharField(max_length=50)
	funcionamientos = FuncionamientoSerializer(many=True)

class FuncionamientoComedorSerializerPost(serializers.Serializer):

	comedor = serializers.IntegerField()
	funcionamientos = FuncionamientoDiaSerializers(many=True)

#class OtrasActividadesComedorSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = OtrasActividadesComedor
#        fields = '__all__' #si quiero todos los campos

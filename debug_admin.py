import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_nutrir.settings')
import django
django.setup()
from encuesta.models import AlimentoEncuesta, Encuesta
from datetime import date, timedelta
from comedor.models import Comedor
from collections import defaultdict

today = date.today()
fecha_limite = today - timedelta(days=365)
lc = Comedor.objects.all()

# Consulta como en el admin
comidas_unicas = AlimentoEncuesta.objects.filter(
    encuesta__fecha__range=(fecha_limite, today), 
    encuesta__comedor__in=lc
).values('encuesta', 'comida__nombre', 'encuesta__fecha__year', 'encuesta__fecha__month', 'etapa_comida').distinct()

print(f'Comidas únicas encontradas: {comidas_unicas.count()}')

# Agrupación como en el admin
encuestas_comidas_meses = defaultdict(lambda: defaultdict(list))

for item in comidas_unicas:
    encuesta_id = item['encuesta']
    etapa_comida = item['etapa_comida']
    comida_nombre = item['comida__nombre']
    year = item['encuesta__fecha__year']
    month = item['encuesta__fecha__month']
    
    encuestas_comidas_meses[encuesta_id][etapa_comida].append({
        'comida_nombre': comida_nombre,
        'year': year,
        'month': month
    })

print(f'Encuestas agrupadas: {dict(encuestas_comidas_meses)}')

# Procesamiento como en el admin
cantidad_raciones_comida_meses = []
for encuesta_id, etapas_comida in encuestas_comidas_meses.items():
    encuesta = Encuesta.objects.get(id=encuesta_id)
    total_comensales = encuesta.cantidad_rango_1 + encuesta.cantidad_rango_2 + encuesta.cantidad_rango_3 + encuesta.cantidad_rango_4
    print(f'Encuesta {encuesta_id}: {total_comensales} comensales')
    
    for etapa_comida, comidas in etapas_comida.items():
        comidas_count = len(comidas)
        print(f'  Etapa {etapa_comida}: {comidas_count} comidas')
        
        if comidas_count > 0:
            comensales_base = total_comensales // comidas_count
            comensales_extra = total_comensales % comidas_count
            
            for i, comida_info in enumerate(comidas):
                raciones_por_comida = comensales_base + (1 if i < comensales_extra else 0)
                print(f'    {comida_info["comida_nombre"]}: {raciones_por_comida} raciones')
                
                cantidad_raciones_comida_meses.append({
                    'encuesta__fecha__year': comida_info['year'],
                    'encuesta__fecha__month': comida_info['month'],
                    'comida__nombre': comida_info['comida_nombre'],
                    'cantidad': raciones_por_comida
                })

print(f'Total items creados: {len(cantidad_raciones_comida_meses)}')
print('Items creados:')
for item in cantidad_raciones_comida_meses:
    print(f'  {item}')

# Agrupación final como en el admin
agrupado = defaultdict(float)
for item in cantidad_raciones_comida_meses:
    key = (item['encuesta__fecha__year'], item['encuesta__fecha__month'], item['comida__nombre'])
    agrupado[key] += item['cantidad']

print(f'Items agrupados: {dict(agrupado)}')

# Convertimos a la estructura esperada
cantidad_raciones_comida_meses_final = [
    {
        'encuesta__fecha__year': year,
        'encuesta__fecha__month': month,
        'comida__nombre': comida,
        'cantidad': round(cantidad, 2)
    }
    for (year, month, comida), cantidad in agrupado.items()
]

print(f'Items finales: {cantidad_raciones_comida_meses_final}')

cantidad_raciones_comida_meses_final.sort(key=lambda x: (x['encuesta__fecha__year'], x['encuesta__fecha__month'], x['comida__nombre']))
comidas = set([item['comida__nombre'] for item in cantidad_raciones_comida_meses_final])
fechas_bd = set([(item['encuesta__fecha__month'], item['encuesta__fecha__year']) for item in cantidad_raciones_comida_meses_final])

print(f'Comidas únicas: {comidas}')
print(f'Fechas únicas: {fechas_bd}')
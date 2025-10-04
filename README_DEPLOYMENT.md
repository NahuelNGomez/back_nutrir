# Guía de Deployment - Backend Nutrir

Esta guía te ayudará a desplegar el backend de Nutrir en un servidor usando Gunicorn y PostgreSQL.

## Requisitos del Sistema

### Versiones Recomendadas
- **Python**: 3.9 (versión específica requerida)
- **PostgreSQL**: 13 o superior
- **Ubuntu/Debian**: 20.04 LTS o superior
- **CentOS/RHEL**: 8 o superior

## 1. Preparación del Servidor

### Instalación de Dependencias del Sistema

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# CentOS/RHEL
sudo yum install python3 python3-pip postgresql-server postgresql-contrib nginx git
```

### Configuración de PostgreSQL

```bash
# Iniciar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear usuario y base de datos
sudo -u postgres psql
```

En la consola de PostgreSQL:
```sql
CREATE DATABASE nutrir;
CREATE USER nutrir_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE nutrir TO nutrir_user;
ALTER USER nutrir_user CREATEDB;
\q
```

## 2. Configuración del Proyecto

### Clonar y Configurar el Entorno

```bash
# Clonar el repositorio (ajustar la ruta según tu caso)
cd /opt/
sudo git clone <tu-repositorio> nutrir-backend
sudo chown -R $USER:$USER /opt/nutrir-backend
cd /opt/nutrir-backend/back_nutrir

# Crear entorno virtual
python3 -m venv env
source env/bin/activate

# Actualizar pip
pip install --upgrade pip
```

### Instalación de Dependencias

```bash
# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# Instalar Gunicorn
pip install gunicorn
```

## 3. Configuración de Variables de Entorno

### Crear archivo .env

```bash
cp django_nutrir/.env_template .env
nano .env
```

Configurar las siguientes variables en el archivo `.env`:

```env
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui
DATABASE_NAME=nutrir
DATABASE_USER=nutrir_user
DATABASE_PASS=tu_password_seguro
DATABASE_HOST=localhost
DATABASE_PORT=5432
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@nutrir.com
DJANGO_SUPERUSER_PASSWORD=tu_password_admin_seguro
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_email
```

**⚠️ IMPORTANTE**: Cambia todas las contraseñas por valores seguros y únicos.

## 4. Configuración de la Base de Datos

### Ejecutar Migraciones

```bash
# Activar entorno virtual
source env/bin/activate

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### Cargar Datos Iniciales

El proyecto incluye comandos personalizados para cargar datos iniciales. Ejecuta los siguientes comandos en orden:

```bash
# 1. Cargar provincias
python manage.py import_provincias --path provincia/management/commands/provincias.csv

# 2. Cargar departamentos
python manage.py import_departamento --path departamento/management/commands/departamentos.csv

# 3. Cargar datos de gobierno local
python manage.py import_gobierno_local --path gobierno_local/management/commands/gobierno_local.csv

# 4. Cargar localidades
python manage.py import_localidad --path localidad/management/commands/localidad.csv

# 5. Cargar tabla SARA de alimentos
python manage.py import_tabla_sara --path alimento/management/commands/tabla_sara.csv

# 6. Cargar horarios de comida
python manage.py poblar_horarios

# 7. Configurar tema personalizado del admin
python manage.py setup_admin_theme

# 8. Cargar grupos de usuarios y permisos
python manage.py loaddata export_grupos.json

# 9. Cargar géneros iniciales (si no existen)
python manage.py shell
```

En la consola de Django, ejecutar:
```python
from genero.models import Genero

# Crear géneros básicos si no existen
generos = ['Masculino', 'Femenino', 'Otro', 'No especifica']
for genero_nombre in generos:
    genero, created = Genero.objects.get_or_create(nombre=genero_nombre)
    if created:
        print(f'Género creado: {genero_nombre}')
    else:
        print(f'Género ya existe: {genero_nombre}')

exit()
```

### Verificar Carga de Datos

```bash
# Verificar que los datos se cargaron correctamente
python manage.py shell
```

En la consola de Django:
```python
from provincia.models import Provincia
from departamento.models import Departamento
from alimento.models import AlimentoSARA
from comida.models import Horario
from genero.models import Genero
from django.contrib.auth.models import Group

print(f"Provincias: {Provincia.objects.count()}")
print(f"Departamentos: {Departamento.objects.count()}")
print(f"Alimentos SARA: {AlimentoSARA.objects.count()}")
print(f"Horarios: {Horario.objects.count()}")
print(f"Géneros: {Genero.objects.count()}")
print(f"Grupos de usuarios: {Group.objects.count()}")
exit()
```

## 5. Configuración de Gunicorn

### Crear archivo de configuración de Gunicorn

```bash
nano gunicorn_config.py
```

Contenido del archivo:

```python
# gunicorn_config.py
import multiprocessing

# Configuración del servidor
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Configuración de logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Configuración de procesos
preload_app = True
daemon = False
pidfile = "/var/run/gunicorn/nutrir.pid"
user = "www-data"
group = "www-data"

# Configuración de archivos estáticos
raw_env = [
    'DJANGO_SETTINGS_MODULE=django_nutrir.settings',
]
```

### Crear directorios de logs

```bash
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R $USER:$USER /var/log/gunicorn
sudo chown -R $USER:$USER /var/run/gunicorn
```

## 6. Configuración de Nginx

### Crear configuración de Nginx

```bash
sudo nano /etc/nginx/sites-available/nutrir
```

Contenido del archivo:

```nginx
server {
    listen 80;
    server_name tu_dominio.com www.tu_dominio.com;

    # Archivos estáticos
    location /static/ {
        alias /opt/nutrir-backend/back_nutrir/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Archivos media
    location /media/ {
        alias /opt/nutrir-backend/back_nutrir/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy a Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Configuración de seguridad
    client_max_body_size 10M;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### Habilitar el sitio

```bash
sudo ln -s /etc/nginx/sites-available/nutrir /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 7. Configuración de Systemd (Servicio)

### Crear servicio de systemd

```bash
sudo nano /etc/systemd/system/nutrir.service
```

Contenido del archivo:

```ini
[Unit]
Description=Nutrir Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/nutrir-backend/back_nutrir
Environment=PATH=/opt/nutrir-backend/back_nutrir/env/bin
ExecStart=/opt/nutrir-backend/back_nutrir/env/bin/gunicorn --config gunicorn_config.py django_nutrir.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Habilitar y iniciar el servicio

```bash
sudo systemctl daemon-reload
sudo systemctl enable nutrir
sudo systemctl start nutrir
sudo systemctl status nutrir
```

## 8. Recopilación de Archivos Estáticos

```bash
# Activar entorno virtual
source env/bin/activate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput
```

## 9. Verificación del Deployment

### Verificar que todo funciona

```bash
# Verificar que el servicio está corriendo
sudo systemctl status nutrir

# Verificar logs
sudo journalctl -u nutrir -f

# Verificar que Nginx está funcionando
sudo systemctl status nginx

# Probar la aplicación
curl http://localhost/admin/
```

### Comandos útiles para mantenimiento

```bash
# Reiniciar la aplicación
sudo systemctl restart nutrir

# Ver logs en tiempo real
sudo journalctl -u nutrir -f

# Verificar configuración de Nginx
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx

# Actualizar archivos estáticos
cd /opt/nutrir-backend/back_nutrir
source env/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart nutrir
```

## 10. Configuración de SSL (Opcional pero Recomendado)

### Usando Certbot (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu_dominio.com -d www.tu_dominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
```

## 11. Backup y Mantenimiento

### Script de backup de la base de datos

```bash
nano /opt/nutrir-backend/backup_db.sh
```

Contenido:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
DB_NAME="nutrir"

mkdir -p $BACKUP_DIR
pg_dump -h localhost -U nutrir_user $DB_NAME > $BACKUP_DIR/nutrir_$DATE.sql
find $BACKUP_DIR -name "nutrir_*.sql" -mtime +7 -delete
```

```bash
chmod +x /opt/nutrir-backend/backup_db.sh
```

### Programar backup automático

```bash
# Agregar al crontab
crontab -e

# Agregar esta línea para backup diario a las 2 AM
0 2 * * * /opt/nutrir-backend/backup_db.sh
```

## 12. Monitoreo y Logs

### Verificar logs importantes

```bash
# Logs de la aplicación
sudo journalctl -u nutrir -f

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs de Gunicorn
sudo tail -f /var/log/gunicorn/access.log
sudo tail -f /var/log/gunicorn/error.log
```

## 13. Actualizaciones del Sistema

### Proceso de actualización

```bash
# 1. Hacer backup
/opt/nutrir-backend/backup_db.sh

# 2. Detener servicios
sudo systemctl stop nutrir

# 3. Actualizar código
cd /opt/nutrir-backend
git pull origin main

# 4. Activar entorno virtual
cd back_nutrir
source env/bin/activate

# 5. Instalar nuevas dependencias
pip install -r requirements.txt

# 6. Ejecutar migraciones
python manage.py migrate

# 7. Recopilar archivos estáticos
python manage.py collectstatic --noinput

# 8. Reiniciar servicios
sudo systemctl start nutrir
```

## Troubleshooting

### Problemas Comunes

1. **Error de permisos**: Verificar que el usuario `www-data` tenga permisos sobre los archivos
2. **Base de datos no conecta**: Verificar configuración en `.env` y que PostgreSQL esté corriendo
3. **Archivos estáticos no se ven**: Verificar configuración de Nginx y ejecutar `collectstatic`
4. **Servicio no inicia**: Revisar logs con `sudo journalctl -u nutrir -f`

### Comandos de diagnóstico

```bash
# Verificar estado de servicios
sudo systemctl status nutrir nginx postgresql

# Verificar puertos
sudo netstat -tlnp | grep :8000
sudo netstat -tlnp | grep :80

# Verificar configuración de Django
cd /opt/nutrir-backend/back_nutrir
source env/bin/activate
python manage.py check
```

## Contacto y Soporte

Para problemas específicos del proyecto, revisar la documentación del código o contactar al equipo de desarrollo.

---

**Nota**: Esta guía asume un servidor Ubuntu/Debian. Para otros sistemas operativos, ajustar los comandos de instalación de paquetes según corresponda.

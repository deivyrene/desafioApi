# Consulta SBIF

_Aplicacion en Django para consultar Api del SBIF_

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

_Que cosas necesitas para instalar el software y como instalarlas_

```
Version de python 3.7, MySQL 5.7, Django 2.1.4
```

### Instalación 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_Pasos_

```
- Clonar el repositorio https://github.com/deivyrene/desafioApi.git

- Luego posicionarse en la carpeta clonada

- Crear un entorno virtual dentro de la carpeta 
  Linux virtualenv env
        source env/bin/activate
        pip install -r requirements.txt
  Windows virtualenv env
          env\scripts\activate
          pip install -r requirements-vendor.txt -t lib/
          pip install -r requirements.txt
          
- Crear una base de datos con nombre desafio

- Ejecutar migraciones: python manage.py makemigrations searchApi
                       python manage.py migrate

- Inicia un servidor web local: python manage.py runserver

- En el navegador web, ingresa la siguiente dirección:http://localhost:8000
```





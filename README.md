Log users/admin Pyramid webApp
=========
Users/passwords: admin/admin, homer/homer, bart/bart, marge/marge, lisa/lisa, maggie/maggie

**Web app hecha con python y el framework pyramid**

- El usuario con rol "admin" se puede loguear, cambiar de rol a los demas usuarios y borrarlos. Postear, borrar sus posts, borrar posts de usuarios. Tambien puede cambiar su foto de perfil.

- Los demas roles pueden: loguarse, postear, editar sus propios posts, borrar sus propios posts y cambiar su foto de perfil.
Los usuarios nuevos se pueden registrar como rol de invitado "guest" y pueden hacer lo mismo que los demas roles excepto lo que puede hacer el admin.
Todos los roles pueden ver los posts de todos.

**CARACTERISTICAS NUEVAS 03/02/2020***
- El administrador puede asignar tareas medidas por tiempo a los usuarios
- Los usuarios pueden iniciarlas, pausarlas y finalizarlas.
- Existe un intervalo del tiempo trabajado que se va acumulando a medida se vaya activando y reanudando la tarea.
- Se muestran las tareas hechas y las que no estan hechas en pantalla y por usuario.
- Lista de usuarios de acceso rapido
- Dos juegos asi como para molestar, un ahorcado muy sencillo y adivinar un numero ultra sencillo.
- Los juegos suman puntaje al usuario.


***author: Martin Vargas***

Español:
---

> **ESTO ES SOLO INFO, SI QUERES PASAR A LA INSTALACION DE LA APP, SALTEA ESTE CUADRO
Cookiecutter es la herramienta que utilize para crear el proyecto NO ES NECESARIO QUE HAGAS ESTE PASO, es solo por si queres empezar un proyecto rapido para Pyramid y es muy recomendable:**
~~~
pip install cookiecutter
cookiecutter gh:Pylons/pyramid-cookiecutter-starter --checkout 1.10-branch
TE VA A SALIR ESTO, EN DONDE ELEGIS EL LENGUAJE DE TEMPLATES (YO USE JINJA2) Y EL BACKEND (USE SQLALCHEMY)
You've cloned ~/.cookiecutters/pyramid-cookiecutter-starter before.
Is it okay to delete and re-clone it? [yes]: yes
project_name [Pyramid Scaffold]: hello_world
repo_name [hello_world]: hello_world
Select template_language:
1 - jinja2
2 - chameleon
3 - mako
Choose from 1, 2, 3 [1]: 1
Select backend:
1 - none
2 - sqlalchemy
3 - zodb
Choose from 1, 2, 3 [1]: 1

cd hello_world <--- te vas a la carpeta del proyecto
python3 -m venv env <--- creas el virtual environment
env/bin/pip install --upgrade pip setuptools <--- actualizas setuptools
env/bin/pip install -e ".[testing]" <--- testeo de requerimientos e instalacion
env/bin/pip install -e .
export VENV=~/hello_world/env <--- resetea la variable de entorno para la nueva que creaste
$VENV/bin/pserve development.ini <--- ejecutas el servidor
$VENV/bin/pserve development.ini --reload <--- para ejecutarlo despues de la primera vez (si queres)
~~~

Para empezar
---
- Para descargar la app podes descargarla desde el boton verde CLONE OR DOWNLOAD, sino desde la terminal:
~~~
git clone https://github.com/apocalipsys/ejerciciopyramid-2020
~~~
**Una vez descargado/clonado seguimos con:**

- Primero tenes que crear una base de datos en Postgresql y cambiar la url en develpment.ini precisamente en la linea 18
~~~
sqlalchemy.url = postgresql://usuario:contraseña@localhost/elnombredelabasededatos
~~~
- Para crear la base de datos, yo uso pgAdminIII para linux
    o sino en la terminal:
~~~
sudo su - postgres
~~~
~~~
psql -U postgres
CREATE DATABASE nombre_db WITH OWNER nombre_usuario;
~~~
- Cambia al directorio del proyecto recién creado.
~~~
    cd ejerciciopyramid-2020
~~~
- Crear un virtual environment de Python.
~~~   
   sudo apt-get install python-virtualenv
   virtualenv --python=/usr/bin/python3.7 venv
~~~
- Activar el virtual environment
~~~
    source venv/bin/activate
~~~    
- Actualizar packaging tools.
~~~
    pip install --upgrade pip setuptools
~~~
- Instalar el proyecto en modo editable con esto se puede testear los requerimientos y dependencias antes de instalarlos
~~~
    pip install -e ".[testing]"
~~~ 
- VERIFICAR SI EDITASTE el archivo development.ini

~~~    
    nano development.ini
~~~
   
   - Linea 18:
~~~
    sqlalchemy.url = postgresql://usuario:contraseña@localhost/elnombredelabasededatos
~~~
    
Inicializar y actualizar la base de datos usando Alembic.
---
- Primero esto:
~~~
    alembic -c development.ini stamp heads
~~~

- Generar la primera revision.
~~~
     alembic -c development.ini revision --autogenerate -m "init"
~~~
- Actualizar esa primera revision.
~~~
     alembic -c development.ini upgrade head
~~~
- Abrir los datos por defecto dentro de la base de datos usando el siguiente script.(se crean varios usuarios y sus            contraseñas son igual a sus nombres(user and pass) admin:admin, homer:homer, bart:bart, lisa:lisa, maggie:maggie y marge:marge
~~~
    initialize_ejerciciokenwin_db development.ini
~~~
- Para ejecutar el proyecto se activa el servidor.
~~~
    pserve development.ini
~~~
- Si necesitas cambiar el puerto lo podes hacer desde el archivo development.ini
--------
Inglish:
--------
Getting Started
---------------
-To CLONE OR DOWNLOAD click on the green button, or put this on terminal:
~~~
git clone https://github.com/apocalipsys/ejerciciopyramid-2020
~~~
**Then:**

- Create a database in Postgresql y change the url en develpment.ini precisamente en la linea 18
~~~
sqlalchemy.url = postgresql://usuario:contraseña@localhost/elnombredelabasededatos
~~~
- To create the database type on terminal:
~~~
sudo su - postgres
~~~
~~~
psql -U postgres
CREATE DATABASE nombre_db WITH OWNER nombre_usuario;
~~~

- Change directory into your newly created project.
~~~
    cd ejerciciopyramid-2020
~~~
- Create a Python virtual environment.

~~~   
   sudo apt-get install python-virtualenv
   virtualenv --python=/usr/bin/python3.7 venv
~~~
- Activate the virtual environment:
~~~
   source venv/bin/activate
~~~ 
- Upgrade packaging tools.
~~~
   pip install --upgrade pip setuptools
~~~
- Install the project in editable mode with its testing requirements.
~~~
   pip install -e ".[testing]"
~~~    
- VERIFY IF YOU EDIT development.ini
~~~    
    nano development.ini
~~~
    
- Line 18:
~~~
    sqlalchemy.url = postgresql://usuario:contraseña@localhost/elnombredelabasededatos
~~~
    

Initialize and upgrade the database using Alembic.
---
- run this before:
~~~
    alembic -c development.ini stamp heads
~~~

- Generate your first revision.
~~~
    alembic -c development.ini revision --autogenerate -m "init"
~~~
- Upgrade to that revision.
~~~
    alembic -c development.ini upgrade head
~~~

- Load default data into the database using a script.
~~~
   initialize_ejerciciokenwin_db development.ini
~~~

- Run your project.
~~~
    pserve development.ini
~~~
# Elemental-Application

## Setup

### Clonar el repo
- mkdir elemental
- cd elemental
- git clone https://github.com/Elemental-LATAM/Elemental-Application.git .

### Requerimientos del proyecto
- instalar versión reciente de django
- virtualenv .venv
- pip install -r requirements.txt
- pip install psycopg2

### Setup del proyecto

#### Migraciones
Para evitar importaciones circulares, aplicar los comandos en este orden: core, members, projects, notes
- python manage.py makemigrations
- python manage.py migrate

#### Estilo
- python manage.py collectstatic

### Start the development server
- python manage.py runserver

### Consideraciones
- Los filtros toman valores por default: programacion y computacion.
- Debes agregar ambos en skill category e interest category respectivamente.
- Los slugs deben ser lowercase sin tildes ni espacios.

## Overview
El proyecto se divide en 5 módulos.

### elemental
Contiene los settings del proyecto y las urls básicas.

### core
Contiene elementos que son compartidos por los otros módulos y las funciones de sesión. También tiene el admin.

### members
Contiene todo lo referente a los miembros de la plataforma.

### projects
Contiene todo lo referente a los proyectos de la plataforma y la relación entre miembros y proyectos (asignación).

### notes
Contiene todo lo referente a mensajes dentro de la plataforma. Notificaciones, peticiones, invitaciones.

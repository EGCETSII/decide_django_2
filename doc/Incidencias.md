# decide-single-estepa-34
* Grupo 2 
* Curso escolar: 2022/2023
* Asignatura: Evolución y gestión de la configuración
## Miembros del equipo:

| Miembro | Implicación |
| ------------- | ------------- |
| [Toledo Vega, Jorge](https://github.com/jvegax) | [10] |
| [Márquez López, José Antonio](https://github.com/josmarlop16) | [10] |
| [Rodríguez García, Luis](https://github.com/LuisUsrDev) | [10] |
| [Díaz López, Diego Jesús](https://github.com/ddiazlop) | [10] |
| [Cáceres Gómez, José](https://github.com/joscacgom) | [10] |
| [Oñate Parra, Julián](https://github.com/jonatep) | [10] |

## Enlaces de interés:
* [Repositorio de código](https://github.com/jvegax/decide/) 
* [Sistema desplegado](https://decide-coral.vercel.app) 

# Gestión de incidencias.
En este documento se detalla el control de incidencias que han ido surgiendo en el proyecto. Todas las incidencias deben seguir la plantilla detallada en la wiki del proyecto

#

## INC-001 - Errores con Decide en Windows
Debido a la dificultad de particionar discos duros para instalar Ubuntu, algunos miembros han intentado ver si era posible instalar Decide en Windows, lo que ha generado algunos problemas de incompatibilidad de versiones.

- Estado: Cerrado.
- Tipo: Fallo.
- Responsable: Oñate Parra, Julián.
- Prioridad: 2

Para solucionar el problema aquellos miembros que tenían problemas particionando el disco duro para instalar Ubuntu usarán un Pen-Drive para realizar allí la instalación del sistema operativo. De esta forma habrá menos problemas de incompatibilidad de versiones.

# 

## INC-002 - Incompatibilidad de versiones en requirements.txt
Las versiones de los módulos a instalar a través del fichero requirements.txt no son correctas, e impiden el inicio de la aplicación.

- Estado: Cerrado.
- Tipo: Fallo.
- Responsable: Toledo Vega, Jorge
- Prioridad: 4

Se han asignado unas nuevas versiones para que el sistema funcione en el despliegue y local. De momento no parece que den más fallos.

# 

## INC-003 - Entornos virtuales incompatibles
Debido al problema descrito en la incidencia INC-002, los entornos virtuales que se habían configurados con versiones de módulos incorrectas ahora tienen más módulos de los necesarios, algunos interfiriéndose entre sí.

- Estado: Cerrado.
- Tipo: Fallo.
- Responsable: Cáceres Gómez, José.
- Prioridad: 2

Se ha determinado que la opción más eficaz que deben adoptar los miembros afectados por este problema es simplemente borrar el entorno virtual que tenían antes, y crear uno nuevo con los nuevos módulos instalados.

# 

## INC-004 - Error al establecer conexión.
Al intentar ejecutar los comandos `./manage.py migrate` o `runserver` no termina con éxito, al haber un error en el intento de conexión.

- Estado: En progreso.
- Tipo: Fallo.
- Responsable: Oñate Parra, Julián.
- Prioridad: 5

## INC-005 - Error con módulo pycryto
El módulo pycrypto ocasiona muchos errores en el proyecto.

- Estado: Cerrado.
- Tipo: Fallo.
- Responsable: Toledo Vega, Jorge.
- Prioridad: 3

Se debe desinstalar el módulo pycrypto e instalar pycryptodome, en la versión especificada en el requirements.txt
  
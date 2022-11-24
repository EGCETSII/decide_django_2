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

### Indicadores del proyecto

Miembro del equipo  | Horas | Commits | LoC | Test | Issues | Incremento |
------------- | ------------- | ------------- | ------------- | ------------- | ------------- |  ------------- | 
[Toledo Vega, Jorge](https://github.com/jvegax) | HH | XX | YY | ZZ | II | Descripción breve 
[Márquez López, José Antonio](https://github.com/josmarlop16) | HH | XX | YY | ZZ | II | Descripción breve 
[Rodríguez García, Luis](https://github.com/LuisUsrDev) | HH | XX | YY | ZZ | II | Descripción breve 
[Díaz López, Diego Jesús](https://github.com/ddiazlop) | HH | XX | YY | ZZ | II | Descripción breve 
[Cáceres Gómez, José](https://github.com/joscacgom) | HH | XX | YY | ZZ | II | Descripción breve 
[Oñate Parra, Julián](https://github.com/jonatep) | HH | XX | YY | ZZ | II | Descripción breve 
*TOTAL* | tHH  | tXX | tYY | tZZ | tII | Descripción breve 

### Integración con otros equipos
Nuestro grupo, al ser single, no ha realizado integración con otros grupos.

## Resumen ejecutivo
Nuestro proyecto se basará en el proyecto de decide, que gestiona un sistema de votaciones a través de Django.
Mediante la integración continua ampliaremos el sistema existente con distintos cambios. Veremos los siguientes apartados:

Descripción del sistema: El sistema al ser un proyecto en Django cuenta con la estructura del mismo: basado en el procesamiento de peticiones HTTP y redirecciones a vistas.

Visión global del proceso de desarrollo: Mediante un ejemplo de los cambios propuestos detallamos el proceso de desarrollo de los mismos. 

Entorno de desarrollo: Se ha optado por utilizar el IDE Visual Studio Code, que ofrece un entorno cómodo y adaptable a Django.

Ejercicio de propuesta de cambio: Mediante un ejemplo se detallará paso a paso cómo implementaremos los cambios en el sistema.

Conclusiones y trabajo futuro: Creemos que podemos mejorar mucho el sistema con estos cambios y adaptaciones.

### Descripción del sistema 
La arquitectura del sistema está basada en el patrón de diseño MVC (Modelo Vista-Controlador), ya que Django aplica este patrón de diseño para procesar sus peticiones. 

El sistema cuenta con varios módulos:

- Routing: Lo más parecido a un controlador. Establece las distintas urls que puede procesar, y para cada una de ellas designa una vista a renderizar, con todos los detalles que sean necesarios.

- View: Procesa las peticiones desde Routing. Puede tener de por sí sólo la vista necesaria a mostrar, pero también puede hacer uso del siguiente módulo. Es el sistema que produce el resultado final, el "response".

- Template: Establece plantillas que pueden utilizar las vistas para renderizarse. 

- Model: Se comunica con la base de datos y la vista. Dependiendo de cada petición y vista, puede obtener datos, que comunica a la vista, y esta los pueden procesar y mostrar.

Veamos paso a paso entonces cómo funcionaría:

1. El servidor se inicia
2. El servidor recibe una URL concreta.
3. Routing recibe la URL, busca que la tenga almacenada, y si es así, envía la información a la vista necesaria.
4. La vista recibe la petición.
4.1. (Opcional) La vista recibe una plantilla desde template para producir la response.
4.2. (Opcional, pero muy frecuente) La vista pide al modelo unos datos concretos que pueden encontrarse en la base de datos.
5. Con todo lo necesario, la vista produce una respuesta, que es lo que se renderiza y muestra al usuario.

Esta es la arquitectura y funcionamiento general de Decide, y no hemos realizado cambios sustanciales a este proceso. Sin embargo, por defecto esta renderización depende sólo de Django o Bootstrap, pero nosotros hemos aplicado React para todo el renderizado de vistas. Pero este cambio no afecta en la arquitectura en sí.

### Visión global del proceso de desarrollo 
Detallaremos el proceso general que el equipo seguirá para implementar los cambios deseados. 

Aspectos generales

- El equipo realizará los cambios en sistemas operativos de Ubuntu o MacOS.
- Si a lo largo de cualquiera de los pasos detallados ocurre algún tipo de incidencia, el miembro del equipo deberá añadirla al registro de incidencias, así como comunicarla al resto de miembros del equipo si no es capaz de resolverla.

Pasos a seguir: 

Preparar sistema

Primero activamos el entorno virtual:

`python3 -m venv nombre-entorno`

`source nombre-entorno/bin/activate`

Clonamos el repositorio

`git clone https://github.com/jvegax/decide.git`

Instalamos las dependencias

`pip install -r requirements.txt`

Si no está aún, crear el usuario en postgres

Aplicar cambios en base de datos

`./manage.py migrate --run-syncdb`

Iniciar servidor

`./manage.py runserver`

Una vez que el servidor está iniciado, si no hay fallos, podemos empezar a desarrollar. Vamos a detallar el ejemplo de, por ejemplo, aplicar el cambio de añadir la opción de leer un Excel para generar el censo.

Primero el miembro crearía una rama nueva en GitHub desde máster, si no se creó aún. El nombre de la rama debe ser corto y debe dejar claro en qué se va a trabajar. En este caso, los comandos serían, desde dentro de la carpeta clonada de Git:

`git pull --all`

`git checkout -b excel-censo`

Abrimos el proyecto en nuestro entorno virtual, que en la mayoría de casos será o PyCharm o Visual Studio Code.

Para VS: 
cd decide
code .

Después de haber modificado los archivos deseados, hay que subir los cambios. Se seguirá la política de commits que se ha propuesto. Por ejemplo, si los cambios realizados de momentos son sólo modificar una vista que añada el botón de leer un Excel:

`git add .`

`git commit -m "chore: modificada vista para leer excels"`

`git push`

Una vez estén todos los cambios terminados a través de GitHub realizamos una Pull-Request desde la nueva rama hacia máster. 

### Entorno de desarrollo 
El equipo ha utilizado mayoritariamente dos entornos de desarrollo: Visual Studio Code y PyCharm.

#### Visual Studio Code.

Se utilizará la versión 1.73.1 para Ubuntu o Mac, según requiera en cada sistema.

Para descargarlo, acceder a la [página web de la versión](https://code.visualstudio.com/updates/v1_73) y seleccionar la versión correspondiente a cada sistema operativo.

Una vez terminado el proceso de instalación hay que añadir varias extensiones necesarias para desarrollar en Django.

Dentro de Visual Studio Code, accediendo a la pestaña "Extensions", o a través del comando Ctrl+Shift+F, buscamos e instalamos los siguientes paquetes, en sus últimas versiones:

- [Django](https://marketplace.visualstudio.com/items?itemName=batisteo.vscode-django)
- [JavaScript (ES6) code snippets](https://marketplace.visualstudio.com/items?itemName=xabikos.JavaScriptSnippets)
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

#### PyCharm

Accedemos a la página web de [PyCharm](https://www.jetbrains.com/es-es/pycharm/download/) y descargamos la versión del sistema operativo adecuado.


### Ejercicio de propuesta de cambio
Se presentará un ejercicio con una propuesta concreta de cambio en la que a partir de un cambio que se requiera, se expliquen paso por paso (incluyendo comandos y uso de herramientas) lo que hay que hacer para realizar dicho cambio. Debe ser un ejercicio ilustrativo de todo el proceso de evolución y gestión de la configuración del proyecto. 

### Conclusiones y trabajo futuro
Como conclusiones, creemos que hemos conseguido mejorar el sistema de Decide presentando un mejor aspecto visual, así como más opciones de accesibilidad y seguridad. 
Para el futuro, podrían añadirse estos cambios:

- Bot de Discord para notificar resultados de votaciones
- Añadir contador con tiempo límite restante para votar

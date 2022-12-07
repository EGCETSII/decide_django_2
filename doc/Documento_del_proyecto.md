- [ ] Explicar el resto de cambios propuestos en el apartado decide
- [ ] Ejercicio de Propuesta de cambio -> Explicar un incremento donde se vea bien los contenidos de la asignatura.

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
[Toledo Vega, Jorge](https://github.com/jvegax) | HH | XX | YY | ZZ | II | Front-end con React 
[Márquez López, José Antonio](https://github.com/josmarlop16) | HH | XX | YY | ZZ | II | Front-end con React
[Rodríguez García, Luis](https://github.com/LuisUsrDev) | HH | XX | YY | ZZ | II | Bot de Telegram 
[Díaz López, Diego Jesús](https://github.com/ddiazlop) | HH | XX | YY | ZZ | II | Traducción del front-end 
[Cáceres Gómez, José](https://github.com/joscacgom) | HH | XX | YY | ZZ | II | Bot de Telegram
[Oñate Parra, Julián](https://github.com/jonatep) | HH | XX | YY | ZZ | II | OAuth2
*TOTAL* | tHH  | tXX | tYY | tZZ | tII | Descripción breve 

### Integración con otros equipos
Nuestro grupo, al ser single, no ha realizado integración con otros grupos.

## Resumen ejecutivo
Nuestro proyecto se basará en el proyecto de decide, que gestiona un sistema de votaciones a través de Django.
Mediante la integración continua ampliaremos el sistema existente con distintos cambios. Veremos los siguientes apartados:

**Descripción del sistema**: El sistema al ser un proyecto en Django cuenta con la estructura del mismo: basado en el procesamiento de peticiones HTTP y redirecciones a vistas.

**Visión global del proceso de desarrollo**: Mediante un ejemplo de los cambios propuestos detallamos el proceso de desarrollo de los mismos. 

**Entorno de desarrollo**: Se ha optado por utilizar el IDE Visual Studio Code, que ofrece un entorno cómodo y adaptable a Django.

**Ejercicio de propuesta de cambio**: Mediante un ejemplo se detallará paso a paso cómo implementaremos los cambios en el sistema.

**Conclusiones y trabajo futuro**: Creemos que podemos mejorar mucho el sistema con estos cambios y adaptaciones.

## Descripción del sistema 

En este apartado realizaremos un análisis de la arquitectura de Django, así como de los subsistemas que tiene Decide.

### Django

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
4.1.(Opcional) La vista recibe una plantilla desde template para producir la response.
4.2. (Opcional, pero muy frecuente) La vista pide al modelo unos datos concretos que pueden encontrarse en la base de datos.
5. Con todo lo necesario, la vista produce una respuesta, que es lo que se renderiza y muestra al usuario.

Esta es la arquitectura y funcionamiento general de Django, y no hemos realizado cambios sustanciales a este proceso. Sin embargo, por defecto esta renderización depende sólo de Django o Bootstrap, pero nosotros hemos aplicado React para todo el renderizado de vistas. Pero este cambio no afecta en la arquitectura en sí.

### Decide

Funcionando bajo esta arquitectura descrita anteriormente, Decide cuenta con varios subsistemas que se comunican entre sí. En el fichero [subsistemas.md](https://github.com/jvegax/decide/blob/master/doc/subsistemas.md) se detallan los subsistemas pre-existentes de Decide. 

Por ello, en este apartado comentaremos o bien cambios que han hemos realizado sobre estos subsistemas, o nuevos que hayamos creado.

#### Autenticación

Queremos que el sistema utilice la tecnología de Oauth2 para que la API sea más segura y eficaz

#### Bot de Telegram

Hemos diseñado un Bot de Telegram que comparte por chat los resultados de las votaciones. 

#### Internacionalización

Se ha hecho uso de [i18next](https://react.i18next.com/latest/trans-component ) para crear un módulo de traducción que permita traducir todo el contenido estático del [front-end](https://github.com/jvegax/decide-front). Este módulo se encuentra organizado dentro del proyecto de la siguiente forma:

````
decide-front   
└───src
│   └───i18n
│       │ index.ts
│       │ types.ts
|       └───languages 
|           | index.ts
|           | de-DE.ts
|           | en-US.ts
|           | es-ES.ts
|           | se-SV.ts
````

En primer lugar, se ha definido dentro de la carpeta *languages* un archivo *index.ts* donde creamos un diccionario para contener todos los lenguajes que soportamos. Además exportamos una lista con estos lenguajes para su uso posterior.

```typescript
import type { Dictionary } from '../types';  
import en_US from './en-US';  
import es_ES from './es-ES';  
import de_DE from './de-DE';  
import se_SV from './se-SV';  
  
const availableLanguages = { en_US, es_ES , de_DE, se_SV};  
  
const languages = Object.entries(availableLanguages).reduce(  
  (acc, [key, value]) => ({  
    ...acc,  
    [`${key}`]: {  
      translation: value,  
    },  
  }),  
  {} as {  
    [id in Language]: Dictionary;  
  },  
);  
  
export type Language = keyof typeof availableLanguages;  
export default languages;
```

En segundo lugar, hemos creado los diccionarios de cada idioma con las palabras estáticas de nuestras vistas. Estos se encuentran dentro de sus respectivos directorios.

```typescript
const dictionary = {  
  voting: 'Voting',  
  login: 'Login',  
  register: 'Register',  
  log_in_to_decide: 'Log in to Decide!',  
  email: 'Email',  
  enter_your_email: 'Enter your email',  
  password: 'Password',  
  enter_password: 'Enter your password',  
  register_to_decide: 'Register to Decide!',  
  name: 'Name',  
  enter_your_name: 'Enter your name',  
  surname: 'Surname',  
  enter_your_surname: 'Enter your surname',  
  confirm_password: 'Confirm password',  
  enter_your_password_again: 'Enter your password again',  
  user_created_successfully: 'User created successfully',  
  some_error_occurred: 'Some error occurred',  
  submit_vote: 'Submit vote',  
  voting_lists: 'Voting lists',  
  cant_login: 'Its not possible to login with these credentials',  
  username: 'Username',  
  enter_your_username: 'Enter your username',  
  passwords_dont_match: 'Passwords dont match',  
};  
  
export default dictionary;
```

En último lugar debemos de declarar en *i18n/index.ts* el idioma por defecto, que en nuestro proyecto será *es_ES (español de ESpaña)* e inicializaremos i18next. De esta forma, el módulo ya es funcional en todos los archivos en los que se especifique mediante:

```typescript
const { t } = useTranslation();
t('[Palabra del diccionario]') // Esto devuelve un AnyType con la traducción de la palabra
```

## Visión global del proceso de desarrollo 
Detallaremos el proceso general que el equipo seguirá para implementar los cambios deseados. 

### Aspectos generales

- El equipo realizará los cambios en sistemas operativos de Ubuntu o MacOS.
- Si a lo largo de cualquiera de los pasos detallados ocurre algún tipo de incidencia, el miembro del equipo deberá añadirla al registro de incidencias, así como comunicarla al resto de miembros del equipo si no es capaz de resolverla.

### Pasos a seguir: 

#### Preparar sistema

Primero activamos el entorno virtual:

`python3 -m venv nombre-entorno`

`source nombre-entorno/bin/activate`

#### Clonamos el repositorio

`git clone https://github.com/jvegax/decide.git`

#### Instalamos las dependencias

`pip install -r requirements.txt`

#### Si no está aún, crear el usuario en postgres

`sudo su - postgres`

`psql -c "create user decide with password 'decide'"`

`psql-c "created atabase decide owner decide"`

La contraseña que pongamos aquí deberá coincidir con la que aparezca en el archivo local_settings.py

#### Aplicar cambios en base de datos

`./manage.py migrate --run-syncdb`

#### Iniciar servidor

`./manage.py runserver`

Una vez que el servidor está iniciado, si no hay fallos, podemos empezar a desarrollar. Vamos a detallar el ejemplo de, por ejemplo, aplicar el cambio de añadir la opción de leer un Excel para generar el censo.

#### Pasos para aplicar cambios

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

## Entorno de desarrollo 
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

Una vez completados todos los pasos, el entorno quedaría listo.

#### PyCharm

Descargaremos la versión 2022.2.2 de PyCharm en la versión necesaria para cada sistema. Para ello, vamos a la [página de su toolbox](https://www.jetbrains.com/toolbox-app/) y la descargamos para el sistema operativo necesario. 

Una vez se descargue, ejecutamos el comando `sudo tar -xzf jetbrains-toolbox-1.17.7391.tar.gz -C /opt` para extraer el contenido.

Ejecutamos el programa de jetbrains-toolbox, y cuando se instale, elegimos de entre las opciones a descargar PyCharm Community, en su versión 2022.02.02

![image](https://user-images.githubusercontent.com/78453718/203844581-aa75ce12-d92f-4ecb-a5df-335b594d5e91.png)

Una vez instalado, ya estaría todo listo.

#### Editor de texto de ubuntu

Aunque es obligatorio que cada miembro del equipo tenga instalado al menos uno de los entornos de desarrollo detallados, cabe mencionar que el uso del editor de texto nativo de ubuntu es una buena opción para hacer ediciones rápidas de todo tipo de archivos: .md para la wiki, páginas de HTML, archivos de Python... Su comodidad e inmediatez pueden llegar a ser útiles en casos puntuales


## Ejercicio de propuesta de cambio
Se presentará un ejercicio con una propuesta concreta de cambio en la que a partir de un cambio que se requiera, se expliquen paso por paso (incluyendo comandos y uso de herramientas) lo que hay que hacer para realizar dicho cambio. Debe ser un ejercicio ilustrativo de todo el proceso de evolución y gestión de la configuración del proyecto. 

## Conclusiones y trabajo futuro
Como conclusiones, creemos que hemos conseguido mejorar el sistema de Decide presentando un mejor aspecto visual, así como más opciones de accesibilidad y seguridad. 
Para el futuro, podrían añadirse estos cambios:

- Bot de Discord para notificar resultados de votaciones
- Añadir contador con tiempo límite restante para votar


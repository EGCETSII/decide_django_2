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

## 👍 INC-001 - Errores con Decide en Windows

| Estado  | Tipo  | Responsable         | Prioridad |
| ------- | ----- | ------------------- | --------- |
| Cerrado | Fallo | Oñate Parra, Julián | 2         |

### Descripción
Debido a la dificultad de particionar discos duros para instalar Ubuntu, algunos miembros han intentado ver si era posible instalar Decide en Windows, lo que ha generado algunos problemas de incompatibilidad de versiones.

### Solución Adoptada
Para solucionar el problema aquellos miembros que tenían problemas particionando el disco duro para instalar Ubuntu usarán un Pen-Drive para realizar allí la instalación del sistema operativo. De esta forma habrá menos problemas de incompatibilidad de versiones.

## 👍 INC-002 - Incompatibilidad de versiones en requirements.txt

| Estado  | Tipo  | Responsable        | Prioridad |
| ------- | ----- | ------------------ | --------- |
| Cerrado | Fallo | Toledo Vega, Jorge | 4         | 

### Descripción 
Las versiones de los módulos a instalar a través del fichero requirements.txt no son correctas, e impiden el inicio de la aplicación.

### Solución Adoptada
Se han asignado unas nuevas versiones para que el sistema funcione en el despliegue y local. De momento no parece que den más fallos.

## 👍 INC-003 - Entornos virtuales incompatibles

| Estado  | Tipo  | Responsable         | Prioridad |
| ------- | ----- | ------------------- | --------- |
| Cerrado | Fallo | Cáceres Gómez, José | 2         |

### Descripción 
Debido al problema descrito en la incidencia INC-002, los entornos virtuales que se habían configurados con versiones de módulos incorrectas ahora tienen más módulos de los necesarios, algunos interfiriéndose entre sí.

### Solución Adoptada 
Se ha determinado que la opción más eficaz que deben adoptar los miembros afectados por este problema es simplemente borrar el entorno virtual que tenían antes, y crear uno nuevo con los nuevos módulos instalados.

## 👍 INC-004 - Error al establecer conexión.

| Estado      | Tipo  | Responsable         | Prioridad |
| ----------- | ----- | ------------------- | --------- |
| Cerrado | Fallo | Oñate Parra, Julián | 5         |

### Descripción 
Al intentar ejecutar los comandos `./manage.py migrate` o `runserver` no termina con éxito, al haber un error en el intento de conexión.

### Solución Adoptada
Modificar el archivo local_settings.py con la información del usuario de postgres.

## 👍 INC-005 - Error con módulo pycryto

| Estado  | Tipo  | Responsable        | Prioridad |
| ------- | ----- | ------------------ | --------- |
| Cerrado | Fallo | Toledo Vega, Jorge | 3         | 

### Descripción 
El módulo pycrypto ocasiona muchos errores en el proyecto.

### Solución Adoptada 
Se debe desinstalar el módulo pycrypto e instalar pycryptodome, en la versión especificada en el requirements.txt

## 👍 INC-006 - Traducción de valores de etiquetas html

| Estado  | Tipo  | Responsable            | Prioridad |
| ------- | ----- | ---------------------- | --------- |
| Cerrado | Fallo | Diego Jesús Díaz López | 2         |

### Descripción 
La forma usual de traducir elementos del frontend no funciona para el contenido de los atributos de una tag de html. Como podría ser el caso de un input:

```typescript
<Input type="text" name={t('enter_your_username_tras')} placeholder={t('username_tras')}  
  value={username} onChange={(e) => setUsername(e.target.value)} />
```

Tanto "name" o "placeholder" no permiten este tipo de práctica a la hora de acceder a la traducción.

### Solución Adoptada 
Declarar constantes con las traducciones parseadas a string dentro del bloque "body" de las funciones que necesiten traducción para atributos de sus tags.

```typeScript
const enter_your_username_tras = t('enter_your_username').toString();  
const username_tras = t('username').toString();
return(
<Input type="text" name={t('enter_your_username_tras')} placeholder={t('username_tras')}  
  value={username} onChange={(e) => setUsername(e.target.value)} />
  )
```

## 👍 INC-007 - Entorno de ubuntu en Windows para su uso en React.js

| Estado  | Tipo  | Responsable            | Prioridad |
| ------- | ----- | ---------------------- | --------- |
| Cerrado | Fallo | Diego Jesús Díaz López | 1         |

### Descripción 
El entorno virtual de ubuntu es necesario en windows para poder ejecutar aplicaciones realizadas con React.js, pero éste requiere de activar la virtualización en la BIOS.

### Solución Adoptada 
Crear una nueva app con npm en un lugar del directorio de archivos diferente al de decide para que éste instale autómaticamente lo necesario para poder ejecutar _npm run dev_.
**Nota:** Es necesario tener instalado Node.js

## 🧨 INC-008 - Conflictos con ramas creadas antes de la internacionalización

| Estado  | Tipo  | Responsable            | Prioridad |
| ------- | ----- | ---------------------- | --------- |
| En progreso  | Github   | Diego Jesús Díaz López | 3        |

### Descripción 
Aquellas ramas del frontend  que han sido creadas antes de la internacionalización presentan conflictos que se deben de resolver de forma ordenada.

### Posibles Soluciones
1. Avisar al responsable de las traducciones para encargarse de las mismas antes de mergear una rama.
2. Antes de realizar la pull request, cada miembro deberá de añadir la internacionalización.

## 🧨 INC-009 - Errores con Decide en MacOs

| Estado      | Tipo  | Responsable                 | Prioridad |
| ----------- | ----- | --------------------------- | --------- |
| En progreso | Fallo | Márquez López, José Antonio | 2         | 

### Descripción 
Debido a que no es posible particionar de manera segura el disco de los MacBook, decidimos probar a ejecutar el proyecto decide en MacOs, lo cual originó bastantes problemas de compatibilidad con respecto a los entornos y demás.

### Posibles Soluciones
Para solucionar el problema, se optó por buscar informacion sobre cada fallo que iba resultando, hasta el punto de que actualmente, al menos dos miembros del equipo pueden ejecutar en proyecto en su MacOs sin problema. 

**No se conocen aun todos los fallos que pueden resultar con respecto a proximas funcionalidades o métodos, por ello se define esta incidencia como en progreso ya que estamos pendientes de proximas evoluciones del proyecto.**

## 🧨 INC-010 - Errores de los tests con el uso de useNavigate

| Estado      | Tipo  | Responsable                 | Prioridad |
| ----------- | ----- | --------------------------- | --------- |
| En progreso | Fallo | Márquez López, José Antonio | 2         | 

### Descripción 
En el front, se utilizaba la funcion "navigate()" propia de react-router-dom, sin embargo, se ha encontrado, que para los tests, esa funcion crea un conflicto.

### Posibles Soluciones
Se han cambiado todos los usos de navigate() donde daban fallos, por redirect() cuyo funcionamiento es exactamente igual.

**No se conocen aun todos los fallos que pueden resultar con respecto a proximas funcionalidades o métodos, por ello se define esta incidencia como en progreso ya que estamos pendientes de proximas evoluciones del proyecto.**
  

